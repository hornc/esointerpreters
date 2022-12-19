#!/usr/bin/perl
# Shameful!
use shame;
use strict;
use warnings;
use Data::Dumper;

use constant MORSE_E => "\.";
use constant MORSE_S => "\.\.\.";
use constant MORSE_M => "__";
use constant MORSE_EXCLAIM => "_\._\.__";

$SIG{'INT'} = 'INT_handler';

# Initialize "The Papers"
my %papers = (-E => '', -S => '', -M => '');
my $esmeraldalang = 1;

print "." . "\n";

if ( $ARGV[0] =~ /^[0-9]+$/) {
	my $n = $ARGV[0];
	my $prompt = "\n$n> ";
	print "Entering N shell $n";
	print "... $prompt";
	while (<STDIN>) {
		$esmeraldalang = 1 - $esmeraldalang if /%esmeraldalang%/;
		$esmeraldalang ? process() : eval;
		print $prompt
	}
} else {
	my $filename = $ARGV[0];
	print "... Loading $filename:\n";
	open(my $fh, '<:encoding(UTF-8)', $filename)
		or die "Could not open file '$filename' $!";
	$/ = "";
	while (<$fh>) {
		s/\|.*//m;
		$esmeraldalang = 1 - $esmeraldalang if /%esmeraldalang%/;
		$esmeraldalang ? process() : eval;
	}
}
end();

sub group_split {
	# split a block into groups of dots or dashes, possibly spanning multiple lines
	# (<char>, (<length>, <# lines>))
	# ('.', (1, 1)), ('_', (2, 1))
	my @groups;
	my $lastc = '';
	my $lastw = 0;
	my $i = -1;
	
	while(m/(([\._ ])\2*($)?)/mg) {
		#print " Checking: $1 ";
		my $c = substr($1, 0, 1);
		my $l = length $1;
		if ($lastc eq $c and $l == $lastw) {
			$groups[$i][2]++;
		} else {
			($lastc, $lastw) = ($c, $l);
			$groups[++$i] = [$c, $l, 1];
		}
	}
	return @groups;
}

sub morse {
	# Taps out ESME into Morse code 
	# so it can be written to the "papers".
	s/ *[Ee]/${\MORSE_E}/g;
	s/ *[Ss]/${\MORSE_S}/g;
	s/[Mm]/${\MORSE_M}/g;
	s/[Éé]/${\MORSE_E}/g;
	s/[!!]/${\MORSE_EXCLAIM}/g;
	return $_;
}

sub process {
	s/^\s+|\s+$//g;
	my $mode = uc substr($_, 0, 1);
	my $jmp = 0;
	morse;
	my $block_size = tr/\._//;
	my $exclamation = () = $_ =~ /${\MORSE_EXCLAIM}/g;
	() = $_ =~ /((${\MORSE_EXCLAIM})+)/g;
        $block_size -= $exclamation * length(MORSE_EXCLAIM);
	if ($exclamation) {
		my $exclamation_last = () = $1 =~ /${\MORSE_EXCLAIM}/g;
		$_ =~ /((${\MORSE_EXCLAIM})+)/;
		my $exclamation_first = () = $1 =~ /${\MORSE_EXCLAIM}/g;
		$block_size -= int($block_size / $exclamation_last * $exclamation_first + 0.5);
	}
	#print "\nRAW BLOCK: [$_]\n";
	#print "\nMODE: $mode\n";
	#print "\nLENGTH: $block_size\n";
	#print "\nMORSE: [$_]\n";
	my @groups = group_split;
	if (0 and $mode eq 'E') {
		print "S GROUPS: " . Dumper @groups;
	}
	my $i = -1;
	while ($i++ < $#groups) {
		#print " I: $i \n";
		my ($s, $x, $y) = ($groups[$i][0], $groups[$i][1], $groups[$i][2]);
		if ($jmp ne 0) {
			$mode = 'E';
			if ($jmp < 0) {
				#print " mode: $mode START AT $i \n";
				my $j = 0;
				while ($jmp <= 0) {
					$jmp += $groups[$i-$j][1] * $groups[$i-$j++][2];
				}
				$i -= $j;
				if ($i < 0) {	
					$i = ~$i; 
				}
				#print " JUMP BACK TO $i \n";
				$jmp =0;
			} else {
				$jmp -= $x * $y;
				next;
			}
		}
		if ($mode eq 'E' and $s eq '.') {
			my $r = my $m = ($i == 0 or $i == scalar @groups - 1) ? -1 : 1;
			my $b = ($x == $y or $i-1 > 0 and ($x == $groups[$i-1][2]) and ($x * $y == $groups[$i-1][1] + $groups[$i-1][2]));  # square!
			$m = 0.5 if $y > $x and not $b;
			($b, $r) = ((1 - $y) * $x, $y) if ($y < $x and $m == 1);
			$b = $y = $y**2 if ($i * $m < 0 and $block_size == ($x**2)/2+$x*$y);  # last block
			$papers{$mode} .= ("Esme " x (int($block_size + $m * ($x * $y + $b)) % 256) . "\n") x abs $r;
		}
		if ($mode eq 'E' and $s eq '_') {
			if (~($x * $y) & 1) {
				$papers{$mode} .= ('Esme ' x 32 . "\n");
			} else {  # Conditional calc jump...
				#print " [Begin JMP CMD] \n";
				$mode = 'S';
			}
		}
		if ($mode eq 'S') {
			if ($s eq '_' and (~$x & 1)) {
				$mode = 'E';
				if ($papers{'S'}) {
					#print $papers{'S'};
					$jmp = () = $papers{'S'} =~ /Esme/mg;
					my $mod = () = $papers{'S'} =~ /!$/mg;
					$jmp *= $papers{'S'} =~ /^!\n/ ? -1 : 1;
					#print "JMP: $jmp \n";
					$papers{'S'} = '!Esme ';
					#print " [JMP COND MET!] ";
				} else {
					# print " [JMP COND _NOT_ MET!] ";
				}
			} else {
				my $log = log($x ** $y) / log 3;
				(my $r, $y, my $n) = int($log) == $log ? (($log - 1) * 3 + ($y > $x), 1, "!") : ($x / 3, $y, $x & 1 ? "" : "!");
				$papers{$mode} .= ($n . "Esme " x (abs($r) * (($s eq '.') ? 1 : 2)) . ($x & 1 ? "\n" : "")) x $y;
			}
		}
		if ($mode eq 'M') {
			$papers{$mode} .= "Esme ";
		}
		if ($mode eq 'E') {
			display_paper($mode);
		}
	}
	# display the M paper
	display_paper('M') if $mode eq 'M';
}

sub display_paper {
	my $mode = $_[0];
	unless ($mode eq 'S') {
		foreach (split(/^/, $papers{$mode})) {
			if ($mode eq 'E' and $papers{'S'}) {
				$papers{'S'} =~ /(.*)(^[^\n]*)$/sm;
				$papers{'S'} = $1;
				if (substr($2, 0, 1) eq "!") {
					$_ .= $2;
				} else {
					s/$2//;
				}
			}
			my $esme = () = /Esme/g;
			print chr $esme;
		}
		$papers{$mode} = '';
	}
}

sub pop_S_paper {
	if ($papers{'S'}) {
		$papers{'S'} =~ /(.*)(^[^\n]*)$/sm;
		$papers{'S'} = $1;
		return $2;
	}
	return;
}

sub INT_handler {
	end();
}

sub end {
	print "\n__\n.\n";
	exit(0);
}
