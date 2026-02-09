#!/usr/bin/env perl
use strict;
use warnings;

binmode STDIN,  ':encoding(UTF-8)';
binmode STDOUT, ':encoding(UTF-8)';

my @th_codes = qw(
  TH-MF TH-IS TH-CD TH-MM TH-UW TH-BS TH-GD TH-AP TH-CM TH-FP
);
my @su_codes = qw(
  SU-AN SU-OB SU-EN SU-HU SU-PA SU-SW SU-BO
);
my @sl_codes = qw(
  SL-MS SL-SS SL-GD SL-CF SL-TD SL-ME SL-AI
);
my @et_codes = qw(
  ET-ME ET-WO ET-UN ET-WH ET-SE ET-DE ET-EC ET-RA
);
my @co_codes = qw(
  CO-BI CO-WO CO-FR CO-SY CO-CU CO-PA CO-DA CO-SP
);

my $th = join q{|}, map { quotemeta } @th_codes;
my $su = join q{|}, map { quotemeta } @su_codes;
my $sl = join q{|}, map { quotemeta } @sl_codes;
my $et = join q{|}, map { quotemeta } @et_codes;
my $co = join q{|}, map { quotemeta } @co_codes;

my $matrix_pattern = qr{
  (?:$th)[ \t]*\+[ \t]*
  (?:$su)[ \t]*\+[ \t]*
  (?:$sl)[ \t]*\+[ \t]*
  (?:$et)[ \t]*\+[ \t]*
  (?:$co)
}x;

my $separator_pattern = qr{[ \t]*(?:\x{2014}|--+|-|:)[ \t]*};

while (my $line = <STDIN>) {
  $line =~ s/^(\s*\d+(?:\.|\))\s*)$matrix_pattern(?:$separator_pattern)?/$1/;
  $line =~ s/^(\s*)$matrix_pattern(?:$separator_pattern)?/$1/;
  print $line;
}
