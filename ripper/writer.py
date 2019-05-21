import os

class Writer(object):

    @staticmethod
    def write(text_or_request,filepath):

        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        
        if isinstance(text_or_request,basestring):
            Writer._write_text(text_or_request,filepath)
        else:
            Writer._write_stream(text_or_request,filepath)

    @staticmethod
    def _write_stream(response,filepath):
        with open(filepath, 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

    @staticmethod
    def _write_text(text,filepath):
        with open(filepath,'w') as w:
            w.write(text.encode('ascii', 'ignore').decode('ascii'))
            w.close()
