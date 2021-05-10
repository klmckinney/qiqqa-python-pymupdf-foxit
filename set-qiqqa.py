import fitz
import hashlib
import json
import logging
import os
import os.path
import sqlite3
import sys
import time

DEFAULT_LIBRARY =  'Z:/_/QIQQA/INTRANET_06147611-5D7C-465D-BD47-B9C77931A7D7'
DEFAULT_FILENAME = '_FB51EFE783F59E2D269BD0A1FD863CEE9582CC.PDF'

if __name__ == "__main__":
    FORMAT = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        filename=(
            "log"
            #"%s %s.log"
            #% (os.path.splitext(sys.argv[0])[0], time.strftime("%Y%m%d-%H%M%S"))
        ),
    )

    logger = logging.getLogger("---START---")
    library  = sys.argv[2] if len(sys.argv) > 2  else DEFAULT_LIBRARY 
    local_pdf_filename = sys.argv[1] if len(sys.argv) > 1  else DEFAULT_FILENAME
    qiqqa_pdf_filename = local_pdf_filename[1:]

    logger.debug("library directory is: {0}".format(library))
    logger.debug("local_pdf_filename is: {0}".format(local_pdf_filename))
    logger.debug("qiqqa_pdf_filename is: {0}".format(qiqqa_pdf_filename))
    pdf = fitz.open(local_pdf_filename)
    full_path_of_library_file = library + "/Qiqqa.library"
    logger.debug("library file: {0}".format(full_path_of_library_file))
    #
    # BUILD a list of dictionaries, one for each annotation
    highlights = []
    for i, page in enumerate(pdf):
        log_i = True
        for annot in page.annots():
            if log_i:
                logger.debug('')
                logger.debug(' page: {0}'.format(i+1))
                log_i = False
            logger.debug(' annot: {0}'.format(repr(annot)))
            logger.debug('  type: {0}'.format(repr(annot.type)))
            logger.debug('  info: {0}'.format(repr(annot.info)))
            if annot.type[0] == 8:
                logger.debug("     rect: {0}".format(repr(annot.rect)))
                if len(annot.vertices) > 4:
                    logger.debug(" vertices: {0}".format(repr(annot.vertices)))
                size = page.mediabox_size
                left = annot.rect.x0 / size[0]
                top = annot.rect.y0 / size[1]
                width = annot.rect.width / size[0]
                height = annot.rect.height / size[1]
                highlight = {"P": i+1, "L": left, "T": top, "W": width, "H": height, "C": 0}
                highlights.append(
                    highlight
                )
    blob = json.dumps(highlights, indent=1).encode("ascii")
    logger.debug(" json: {0}".format(repr(blob)))
    _md5 = hashlib.md5()
    _md5.update(blob)
    _md5 = _md5.hexdigest().upper()
    logger.debug("md5: {0}".format(_md5))

    c = sqlite3.connect(full_path_of_library_file)
    c.execute(
        """REPLACE INTO LibraryItem (fingerprint, extension, md5, data, last_updated) VALUES (?,?,?,?,?)""",
        (os.path.splitext(qiqqa_pdf_filename)[0], "highlights", _md5, blob, None),
    )
    c.commit()
    c.close()

    logger.debug("")
