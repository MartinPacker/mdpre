
import sys

import mdpre # TODO: fix this later 

def test_stdout_g_output():
    g_output_stdout = mdpre.create_output_file()
    g_output_stdout.writeMarkdown('| sys.stdout works\n')
    mdpre.exit_script(g_output_stdout, 0)
    
def test_file_g_output():
    g_output_file   = mdpre.create_output_file('test.md')
    g_output_file.writeMarkdown('| file output works\n')
    mdpre.exit_script(g_output_file, 0)

if __name__ == "__main__":
    test_stdout_g_output()
    test_file_g_output()