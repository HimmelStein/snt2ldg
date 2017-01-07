
Corpus Documentation for the Multiple-Translation Chinese Corpus (MTC)


Project Goal:

To support the development of automatic means for evaluating
translation quality, the LDC was sponsored to solicit 11 sets of human
translations for a single set of Mandarin Chinese source materials.
The LDC was also asked to produce translations from whatever MT
systems are commercially available or for free from the Internet.


Source Data Selection:

Three sources of journalistic Mandarin Chinese text were selected from
existing LDC corpora:

 - Xinhua News Service: 52 news stories
 - Zaobao News Service: 27 news stories
 - Voice of America Mandarin broadcast transcripts: 26 news stories
(total: 105 stories)

The Xinhua data were drawn from the "Chinese Treebank Corpus"
(LDC2001T11); the file names and "doc_id" attributes assigned to these
stories match the file names used in the Chinese Treebank release.

The Zaobao and VOA data were both drawn from the "TDT3 Multilanguage
Text Corpus" (LDC2001T58); their file names and "doc_id" attributes
match the "DOCNO" tags assigned to these stories in the TDT3 release.

Selection of stories from the two newswire collections was controlled
by story length: all selected stories contain between about 340 and
400 Chinese characters.  The selection from VOA broadcasts varied more
widely, between 100 and 1000 characters per story.  The overall count
of Chinese characters by source is shown in Table 1.

Table 1: Total Number of Chinese Characters, by source

Xinhua	 20626
Zaobao	 11337
VOA	  9256
--------------
total	 41219


The VOA Mandarin transcripts in TDT3 were created manually by a
professional transcription service, but with limited editorial quality
control -- while generally quite complete, these transcripts were not
expected to exceed the quality or accuracy of closed-caption text in
television broadcasts.

Zaobao is a news portal from Singapore and many of its news stories
are translations from other news agencies' releases.


Source Data Preparation for Human Translation:

As published in the existing LDC corpora, the original source files
used GB-2312 encoding for the Chinese characters, and SGML tags for
marking sentence and paragraph boundaries and other information about
each story.  The character encoding has been left unaltered.  To make
things easier for translators, nearly all sgml tags were removed, or
replaced by "plain text" markers.  Specifically, each story was
presented to the human translators in the following format:

 <MT_input source_language="Chinese" doc_ID="...">

 -Headline-
 {Chinese text to be translated}

 -Paragraph-
 -Segment-
 {Chinese text to be translated}
 ...

 </MT_input>

(Note that the -Headline- marker was never used in the VOA stories.)
Each -Segment- corresponds to a Chinese sentence.  The rationale for
using the term "segment" instead of "sentence" was to discourage the
translator from inserting additional "-Sentence-" markers if a Chinese
sentence is translated as two or more English sentences.  The markers
were intended to assure that the resulting translations would be
easily alignable to the source texts, so extra care was taken to make
sure that they would be kept intact and properly oriented.

Some cleaning had to be done for all the files to conform to the above
format, including:

 * adding -Segment- tags to Xinhua and Zaobao files that did not have
   <s> tags in the existing SGML format;

 * adding -Paragraph- tags to VOA files;

 * correcting wrong characters and splitting very long segments into
   smaller chunks in VOA transcripts.

As a last step, all files were converted from UNIX-style line
termination (new-line only) to MS-DOS-style (carriage-return plus
line-feed), on the assumption that most (possibly all) translators
would use MS-Windows-based editors.


Human Translation Procedure and Quality Assessment:

Each initially selected translation team received the translation
guidelines and a sample pair of source and translation (excluded from
the final release) for review.  After the team said that they
understood the task requirements and would be willing to participate
in the project, the 52 Xinhua news stories were sent to them as a
first installment of data .

In accordance with the guidelines, each translation team was asked to
return the first 10 Xinhua stories for quality checking.  This was to
ensure that the translation team had indeed understood and was
following the guidelines and the translation quality was acceptable.
The LDC sent the translations back to the translation team for any
deviations from the guidelines or quality issues detected.

Subsequent translation submissions were continuously monitored for
conformance and quality.  Once the full set of translations was
complete, a final pass of reformatting and validation was carried out,
to assure alignability of segments, and to convert the translated
texts into SGML format.

Each translation team was also asked to fill out and return a
questionnaire to describe their procedures and professional
background.  This information is summarized in tabular form in the
file "trans_team.info".


Machine Translation Procedure:

Complete sets of automatic MT translations were also produced by
submitting the 105 stories to each of 6 publicly-available MT systems.
Four of these were commercial MT software packages (off-the-shelf
products), and 2 were free web-based services.  Starting from the
original SGML text format, special alterations were made to the files
on an as-needed basis, so that they would be accepted and handled
correctly by the various systems; also, the systems differed in terms
of the input and retrieval methods required to submit the source data
for translation and to save the translated text in alignable form.
Additional details are provided in the file "trans_team.info".


Final Data Format and Validation:

For the present release, the corpus content is organized into "source"
and "translation" directories.  Within "translation" there is a
separate subdirectory for each translation service or system,
identified as follows:

   Human translators:	ta0 ta1 ta2 ta3 ta4 ta5 ta6 ta7 ta8 ta9 tb0
   Automatic systems:	tb1 tb2 tb3 tb4 tb5 tb6

The source directory and each of the translation subdirectories
contains 105 files, one news story per file.  Corresponding file names
are identical across all directories, consisting of "doc_id.sgm".

Within each source file, the content is formatted in SGML as follows:

  <DOC doc_id="...">
  <hl>
  <seg id=1> [Chinese text in GB character encoding] </seg>
  </hl>
  <p>
  <seg id=2> [Chinese text in GB character encoding] </seg>
  </p>
  ...
  </DOC>

Notes:

 * the doc_id string enclosed in double quotes matches the file name

 * the VOA files do not have <hl> tags, only <p> and <seg>

 * the <seg> tags are always assigned sequential numeric ID's
   starting at 1 for the first <seg> of each file, are always
   placed on the same line with their contents, and are always
   separated from the contents by a space.

The content of the translation files is identical to the source files
except:

 * the initial <DOC> tag contains an additional attribute:

   <DOC doc_id="..." sys_id="...">

   where the sys_id string enclosed in double quotes matches the name
   of the directory containing the file

 * the contents of the <seg> tags are plain ASCII English text,
   although most of the automatic MT systems included some strings of
   untranslated GB character data in their output, and these are
   retained as-is (see "trans_team.info" for more details)

To verify that all the files conformed to this SGML specification, and
were fully alignable at the level of segments, a custom validation
script (validate.perl) was written to perform a rigorous check across
the entire corpus.  The script produced four output listings:

 * filelist.source: lists source files and segments per file

 * filelist.translation: lists translation files and segments per file

 * validate.log: complete tabulation of segment sizes

 * validate.err: lists empty translation segments (path/doc_id,seg_id)
		 and files containing any untranslated Chinese text

Each line of the validate.log file represents one segment in the set
of 105 stories (there are a total of 993 segments).  The columns
provide the file name (doc_id), the segment number (seg_id), and for
each version of the file (source and 17 translations), the number of
bytes and number of space-separated tokens found in that version of
the segment.  Column headings are provided in the first line of the
log file, and each line is about 192 characters wide.

The validate.err file reports two kinds of problems in the translated
files:

 * no text in a segment
 * one or more segments with untranslated Chinese/GB content in a file

There are 22 occurrences of the former problem, and 466 occurrences of
the latter; most of these are due to the machine-translation system
outputs.


Ranking of Manual Translations:

At the point when only the Xinhua translations had been received from
the various translation services, an initial ranking was performed by
two LDC personnel, one a Chinese-dominant bilingual and the other an
English-dominant bilingual.  There was overall agreement on the
ranking between the two and minor discrepancies were resolved through
discussion and comparison of additional files.  This initial ranking
among the manual translations is:

 best							    worst
 ta0 > ta4 > ta1 > ta2 > ta3 > ta5 > ta6 > ta7 > ta8 > ta9 > tb0

The ranking method was unstructured and somewhat casual -- it is not
intended to be definitive, or even accountable.  A more systematic
assessment of translation quality, using 10 judges and a formal
protocol, is to begin as this data set is published, and the results
of that assessment will be released subsequently.


------------------------------------
David Graff, graff@ldc.upenn.edu
Shudong Huang, shudong@ldc.upenn.edu
January 24, 2002

