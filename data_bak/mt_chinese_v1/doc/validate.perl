#!/usr/bin/perl

# Program:	validate.pl
# Written by:	dave graff
# Purpose:	scan both source-text and human-translation-text
#		files to validate the latter against the former.

# For the MT data creation project, a set of text files in a given
# language (Chinese, Arabic, ...) is selected and formatted for
# presentation to several selected translation services.  Each service
# is expected to return English translations of the complete text set,
# preserving the structural divisions of text (headlines, paragraphs
# and "segments") that were explicitly marked in the source-language
# text files.

# This program assumes that the source-language texts are in a
# directory called "source" and the translations are in a directory
# called "translation", which has separate subdirectories for each
# source of translation data (each translation "system").  Within the
# "source" and "translation/system" directories, each individual data
# file contains one story (DOC unit).  Each "translation/system"
# subdirectory should reflect the contents of "source" exactly, the
# only difference being the data content enclosed within "<seg>" tags.

die "Can't find 'source/' and 'translation/' in CWD ($ENV{PWD})\n"
    unless ( -d "source" && -d "translation" );

# make sure there is an up-to-date file list, showing number of
# segments in each file, for both source and translation sets:

if ( -e "filelist.source" ) {
    @newer = `find source -follow -newer filelist.source`;
    unlink "filelist.source" if ( @newer );
}
if ( -e "filelist.source" ) {
    @srcs = `cat filelist.source`;
    map { ($file,$scnt) = split;
	  $ref{$file}{NSEG} = $scnt;
	  $nlen = length($file) if ($nlen<length($file)); } @srcs;
} else {
    &mkSrcInfo;
}

if ( -e "filelist.translation" ) {
    @newer = `find translation -follow -newer filelist.translation`;
    unlink "filelist.translation" if ( @newer );
}
if ( -e "filelist.translation" ) {
    @trns = `cat filelist.translation`;
    map { ( $sysfile, $scnt ) = split;
	  ($sys,$fid) = split( /\//, $sysfile, 2 );
	  $trn{$sys}{$fid}{NSEG} = $scnt; } @trns;
} else {
    &mkTrnInfo;
}

# conduct syntax checks and per-segment length/token counts on all files

foreach $sys ( sort keys %trn ) {
    foreach $file ( sort keys %{$trn{$sys}} ) {
	&getTknInfo( "translation/$sys/$file", \%{$trn{$sys}{$file}} );
    }
}

# print column headings for output table

$colfmt = "%-".$nlen."s %3d %4d/%-2d ";
$hdrfmt = "%-".$nlen."s seg  source  ";
printf( $hdrfmt, "#bytes/tokens  file" );
foreach $sys ( sort keys %trn ) {
    printf( " %-8s", $sys );
}
print "\n";

foreach $file ( sort keys %ref ) {
    &getTknInfo( "source/$file", \%{$ref{$file}} );

# report segment counts, segment lengths and token counts of source and translation files

    for ( $i=1; $i<=$ref{$file}{NSEG}; $i++ ) {
	$out = sprintf( $colfmt, $file, $i, $ref{$file}{SLEN}[$i], $ref{$file}{TKNS}[$i] ); 
	foreach $sys ( sort keys %trn ) {
	    $out .= sprintf( " %4d/%-3d", $trn{$sys}{$file}{SLEN}[$i], $trn{$sys}{$file}{TKNS}[$i] );
	}
	print "$out\n";
    }
}

sub getTknInfo
{
    ( $path, $hash ) = @_;

    @line = `egrep '</?[Ds]' $path`;
    warn "$path: bad or missing DOC tags\n"
	unless ( $line[0] =~ /^<DOC docid=[-\".\w]+/i && $line[$#line] =~ m:^</DOC>$: );
    $nonascii = 0;
    for ( $i=1; $i<$#line; $i++ ) {
	if ( $line[$i] =~ m%^<seg id=$i>\s*(\S[^<]+)</seg>\s*$% ) {
	    $txt = $1;
	    $txt =~ s/\s*$//;
	    $txt =~ s/\s+/ /g;
	    $hash->{TKNS}[$i] = scalar( split( / /, $txt ));
	    $hash->{SLEN}[$i] = length( $txt );
	    $nonascii++ if ( $txt =~ /[^\s!-~]/ );
	} else {
	    $err = ( $line[$i] =~ m%^<seg id=$i>\s*</seg>% ) ?  "no text" : "bad format";
	    warn "$path: $err at segment $i\n";
	    $hash->{TKNS}[$i] = $hash->{SLEN}[$i] = 0;
	}
    }
    warn "$path: non-ascii content in $nonascii segments\n" if ( $path =~ /translation/ && $nonascii );
}

sub mkSrcInfo	# generate reference list for source files (filename, number of segments)
{
    @srcfiles = `find source -follow -type f`;
    open( L, ">filelist.source" );
    foreach ( sort @srcfiles ) {
	chop;
	( $s, $fid ) = split( /\// );
	$ns = `grep -c '<seg' $_`;
	print L "$fid\t$ns";
	chop $ns;
	$ref{"$fid"}{NSEG} = $ns;
	$nlen = length($fid) if ($nlen<length($fid));
    }
    close L;
}

sub mkTrnInfo	# generate reference list for translations (system, filename, number of segments)
{
    @srcfiles = `find translation -follow -type f`;
    open( L, ">filelist.translation" );
    foreach ( sort @srcfiles ) {
	chop;
	( $t, $sysid, $fid ) = split( /\// );
	$ns = `grep -c '<seg' $_`;
	chop $ns;
	$trn{$sysid}{"$fid"}{NSEG} = $ns;
	print L "$sysid/$fid\t$ns\n";
	if ( exists( $ref{"$fid"}{NSEG} )) {
	    warn "$sysid/$fid: found $ns segs, expecting " . $ref{"$fid"}{NSEG} . "\n"
		if ( $ns != $ref{"$fid"}{NSEG} );
	} else {
	    warn "$sysid/$fid: no corresponding docid in source\n";
	}
    }
    close L;
}
