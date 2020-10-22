
import sys

import mdpre # TODO: fix this later 

def test_stdout_writer():
    writer_stdout = mdpre.create_output_file()
    writer_stdout.writeMarkdown('| sys.stdout works\n')
    mdpre.exit_script(writer_stdout, 0)
    
def test_file_writer():
    writer_file   = mdpre.create_output_file('test.md')
    writer_file.writeMarkdown('| file output works\n')
    mdpre.exit_script(writer_file, 0)

if __name__ == "__main__":
    test_stdout_writer()
    test_file_writer()