#!/usr/bin/env python


import os
import sys

#  GC stands for Git Control 
#  script to automate many files adding to git
#  excluding files from adding to index
#  tracking specifically WITHOUT having to know
#  much of git commands

#  put the files to track on indexed_files list below

#   branch_name is always gonna be arg no. 1
#   msg format to be used:
#
#   in the terminal:
#   note the symbols | and ~ are necessary for the working of this script
#   '~' signifies commit
#   and | signifies index addition for commit
#   ....$ ./gc.py <branchname> "|<filenames_separated_by_spaces>~<commit_message>"

branch_name = sys.argv[1]

if len(sys.argv)<3:
    #signifies only a checkout
    print("Hit the bash for a checkout\nDon't waste my effort. :-(")
    sys.exit(0)

indexed_files = [
    'main.py',
    'gc.py',
    'pix.kv'
]



class Parse_Command:
    def __init__(self, msg=None):
        if msg==None:
            print("Arguments are required")
            sys.exit(1)
        else:
            self.msg = msg.strip()
        
        if self.get_info():
            self.parse_msg()
        else:
            print("No operation specified")
            sys.exit(1)
    
    def get_info(self):
        
        self.addindex = self.commit =self.both_optn = False
        self.addindex_only = self.commit_only = False
        if '|' in self.msg:
            self.addindex = True
        if '~' in self.msg:
            self.commit = True
        
        if self.addindex and (not self.commit):
            self.addindex_only = True
        elif self.commit and (not self.addindex):
            self.commit_only = True
        elif self.addindex and self.commit:
            self.both_optn = True

        #return True if any one operation is present
        #else no need to continue executing the script
        #if no operation is specified 
        #then print err msg and exit
        return (self.addindex_only or self.commit_only or self.both_optn)


    def parse_msg(self):

        def get_commit_msg():
            return (self.msg[self.msg.find('~')+1:]).strip()

        def get_index_files():
            if '~' in self.msg:
                index_files = (self.msg[self.msg.find('|')+1:self.msg.find('~')]).strip().split()

            else:
                index_files = (self.msg[self.msg.find('|')+1:]).strip().split()

            index_files = self.check_files_exist(index_files)
            return index_files
        
        def get_both_msgs():
            index_files = get_index_files()
            commit_msg = get_commit_msg()
            return (index_files, commit_msg)


        if self.commit_only:
            self.commit_msg = get_commit_msg()
        elif self.addindex_only:
            self.index_files = get_index_files()
            
            #if the user wants to both add and commit
        else:
            #if both were false, the program would have
            #already exited above----------------------
            #if both commit and index are given this function executes

            #suppose user entered the msg: |~SomeCommitMsg
            #the following check is necessary
            self.index_files, self.commit_msg = get_both_msgs()

    def check_files_exist(self, files):
        files_found = []
        if files or indexed_files:
                files_found = indexed_files + files
                for file in files_found:
                    if os.path.exists(file)==False:
                        print("One or more files don't exist")
                        print("Please check your index list")
                        sys.exit(0)


                return files_found
        else:
            print("No files to add")
            sys.exit()
    
    def execute(self):
        checkout = "git checkout {}".format(branch_name)
        add_index = 'git add {}'
        commit='git commit -m "{}"'
        both_operation = self.And(add_index, commit)
        execution = ''
        files_to_add = (' '.join(self.index_files)).strip()

        if self.commit_only:
            commit = commit.format(self.commit_msg)
            execution = self.And(checkout, commit)
        
        elif self.addindex_only:
            execution = add_index = add_index.format(files_to_add)

        elif self.both_optn:
            execution = self.And(checkout.format(branch_name),
                             both_operation.format(
                                 files_to_add,
                                 self.commit_msg
                                )
                             )

        os.system(execution)


    def And(self, string1, string2):
        return string1+'&&'+string2
        
git_info = Parse_Command(sys.argv[2])

if __name__ == '__main__':
    git_info.execute()