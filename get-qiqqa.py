import fitz
import json
import logging
import os
import os.path
import sqlite3
import sys
import time


DEFAULT_LIBRARY =  'Z:/_/QIQQA/INTRANET_06147611-5D7C-465D-BD47-B9C77931A7D7'
DEFAULT_FILENAME = 'FB51EFE783F59E2D269BD0A1FD863CEE9582CC.PDF'

if __name__ == '__main__':
    FORMAT = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        filename=("%s %s.log" % (os.path.splitext(sys.argv[0])[0], time.strftime("%Y%m%d-%H%M%S"))),
    )

    logger = logging.getLogger("---START---")
    library  = sys.argv[2] if len(sys.argv) > 2  else DEFAULT_LIBRARY 
    filename = sys.argv[1] if len(sys.argv) > 1  else DEFAULT_FILENAME

    logger.debug('library directory is: {0}'.format(library))
    logger.debug('filename is: {0}'.format(filename))

    logger.debug('locating file within library directory')
    for dir, subdir, filenames in os.walk(library):
        filenames_upper = [x.upper() for x in filenames]
        if filename.upper() in filenames_upper:
            pdf_filename = os.path.join(dir, filename)
            logger.debug('pdf_filename: {0}'.format(pdf_filename))
            pdf = fitz.open(pdf_filename)
            full_path_of_library_file = library + '/Qiqqa.library' 
            logger.debug('library file: {0}'.format(full_path_of_library_file))
            c = sqlite3.connect(full_path_of_library_file)
            query_string = "select * from LibraryItem where fingerprint = '%s' and extension='highlights'" % (os.path.splitext(filename)[0])
            logger.debug('query_string: {0}'.format(query_string))
            rows = list(c.execute(query_string))
            logger.debug('highlights: ' + repr(rows))
            if rows:
                logger.debug('*** HIGHIGHTS FOUND')
                highlights = json.loads(rows[0][3])
                logger.debug('highilghts: {0}'.format(highlights))
                
                #TODO-2: Convert into annotations for local PDF
                for i,highlight in enumerate(highlights):
                    logger.debug('highlight {0}: {1}'.format(i, repr(highlight)))
                    page = pdf[highlight['P']-1]
                    size = page.mediabox_size
                    x0 = highlight['L'] * size[0]
                    y0 = highlight['T'] * size[1]
                    x1 = x0 + highlight['W'] * size[0]
                    y1 = y0 + highlight['H'] * size[1]
                    rect = fitz.Rect(x0,y0,x1,y1)
                    logger.debug('rect: {0}'.format(repr(rect)))
                    annot = page.addHighlightAnnot(rect)
                    #
                    #This followwing "set_rect" is necessary.  I am  not entirely sure why
                    # "addHighlightAnnot" doesn't set the rect exactly as specified. Or
                    # it could be that this is a Qiqqa/MuPDF difference and this is 
                    # "band-aiding" the fundamental problem.
                    annot.set_rect(rect) 
            else:
                logger.debug('!!! NO HIGHLIGHTS FOUND !!!')
            pdf.save('_' + filename)
            logger.debug("")
            break
    else:
        logger.debug('library file could not be found')
        print("file not found!")
        sys.exit(-1)

