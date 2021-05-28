This is a repository of my experimentations with merging PDF
annotations as done with FoxIt into
[QIQQA](https://github.com/jimmejardine/qiqqa-open-source) and also
experimenation with [MuPDF](https://github.com/ArtifexSoftware/mupdf).
I am making this visible on GITHUB to facilitate collaboration with
the QIQQA project.

# Intent / What does this do?

PDF annotations feature prominently in my workflow as these provide a
rich annotation feature set. Currently Qiqqa only supports a few
annotation types in its own application, which are stored in its
SQLite-based metadata database; meanwhile I like to use other
applications (e.g. [FoxIt](https://www.foxitsoftware.com/pdf-editor/))
which enable me to edit PDF annotations directly.

Qiqqa currently has no means to easily export PDFs for annotation
editing in third-party applications and then re-importing and
incorporating the annotation edits done.

These python scripts have been created to

- allow one to access the SQLite metadata directly, take a PDF
  document and augment it with its Qiqqa/database-stored annotations
  to date and have that ready for review and annotation editing in
  your preferred application
  ([FoxIt](https://www.foxitsoftware.com/pdf-editor/), [PDF
  Annotator](https://www.pdfannotator.com/en/), ...)
- pick up the *annotated* PDF document, extract the annotations and
  plug them into the Qiqqa SQLite metadata database directly for
  persistence. The annotated PDF is to be discarded afterwards, as the
  next iteration will re-create the PDF from the Qiqqa database.


## Technology notes



Qiqqa uses a database record format for the annotations which includes
an MD5 hash over the record data. The import script properly creates
this hash to ensure that Qiqqa will recognize the new annotation
records as valid.



## Caveats

As the import script directly accesses the SQLite database for writing
(annotation records), it is **mandatory** to close and exit your Qiqqa
application **before** you run this script as SQLite is not engineered
for multi-process access: if you don't, database corruption may result
from this simultaneous write access.

Qiqqa is yet unable to paint / show many types of PDF annotation in
its own UI.  This repository "skips" that issue and just focuses on
how the annotations will work with "external" PDF viewers, not Qiqqa
itself.

I anticipate further work in the Qiqqa repository after I work out
issues here.

