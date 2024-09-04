from util_models.PDF import PDF
class Session:

    def __init__(self, net=None, protect=None, access=None):
        self.ubnt_net = net
        self.ubnt_protect = protect
        self.ubnt_access = access
        self.pdf = PDF()

    def generate_pdf(self, title='', author='',output_file_name='', chapters=[]):
        chap_num = 0
        
        try:
            self.pdf.set_title(title)
            self.pdf.set_author(author)
            for chapter in chapters:
                chap_num+=1
                self.pdf.print_chapter(chap_num, chapter['name'], json.dumps(chapter))
            self.pdf.output(output_file_name)
        except Exception as e:
                print(e)
        else:
                print('PDF Report Creation Complete')

