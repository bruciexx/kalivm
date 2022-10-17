#!/usr/bin/env python
'''
A small python script for creating/destroying a Kali VM using Vagrant
'''
import sys
import argparse as ap
import time as t
import os

'''
runs shell commands using bash
'''
def sh(script):
    os.system("bash -c '%s'" % script)

p = ap.ArgumentParser(description='A quick kali vagrant setup')
p.add_argument('-command', '-c', help='use "machineup" or "init" to creat a kali vm and start it, and use "machinedown" or "destroy" to destroy it')

# p.add_argument('-up', '-u', '--machine-up')

arg = p.parse_args()

'''
replaces <oldstring> in <infile> with <newstring> and outputs to <outfile>
'''
def replace_string_in_file(infile, outfile, oldstring, newstring):
    with open(infile, 'rt', encoding="utf-8") as fin:
        with open(outfile, 'wt', encoding="utf-8") as fout:
            for line in fin:
                if oldstring in line:
                    fout.write(line.replace(oldstring, newstring))
                else:
                    fout.write(line)

'''
overwrites the vagrantfile to change vm-memory and turn gui on/off
'''
def overwrite_vagrantfile():
    ### Set booleaan default value to false
    guiboolean = 'false'

    ### Set the amount of memory to use for the machine
    memory = input('Do you want to use 1024, 2048, 4096 or more MBs of RAM?  >')
    if memory == '':
        temp_bool = input("Do you want to use the default amount (4096MB)? (Y/n)  >")
        if temp_bool == '' or temp_bool == 'y' or temp_bool == 'Y':
            memory = '4096'
            print('using ' + str(memory) + ' MBs of memory')
        else:
            print('something went wrong, please re-run the command and try again.')
            sys.exit()
    else:
        print('using ' + str(memory) + ' MBs of memory')

    ### Set the amount of CPUs to use for the machine
    cpus = input('How many CPUs would you like to use?  >')
    if cpus == '':
        temp_bool = input("Do you want to use the default amount (2)? (Y/n)  >")
        if temp_bool == '' or temp_bool == 'y' or temp_bool == 'Y':
            cpus = '2'
            print('using ' + str(cpus) + ' CPU cores')
        else:
            print('something went wrong, please re-run the command and try again.')
            sys.exit()
    else:
        print('using ' + str(cpus) + ' CPU cores')

    ### Set the vb.gui boolean to configure the gui or not
    headlessornot = input('Do you want your machine headless? (y/N)  >')
    if headlessornot == 'y' or headlessornot == 'Y':
        guiboolean = 'false'
    elif headlessornot == 'n' or headlessornot == 'N' or headlessornot == '':
        guiboolean = 'true'
    else:
        print('something went wrong, please re-run the command and try again.')
        sys.exit()

    ### Set a boolean for deciding if the user wants to update or not
    update_bool = input('Do you want to update the machine? (y/N)  >')
    if update_bool == 'y' or update_bool == 'Y':
        update_bool = True
    elif update_bool == 'n' or update_bool == 'N' or update_bool == '':
        update_bool = False
    else:
        print('something went wrong, please re-run the command and try again')
        sys.exit()

    ### Hard-coding the strings that need to be changed
    oldstring_1 = '# config.vm.provider "virtualbox" do |vb|'
    oldstring_2 = '#   vb.gui = true'
    oldstring_3 = '#   vb.memory = "1024"'
    oldstring_4 = '# end'
    oldstring_5 = '# config.vm.provision "shell", inline: <<-SHELL'
    oldstring_6 = '#   apt-get update'
    oldstring_7 = '#   apt-get install -y apache2'
    oldstring_8 = '# SHELL'

    ### Setting the new strings that are gonna replace the old ones
    newstring_1 = ' config.vm.provider "virtualbox" do |vb|'
    newstring_2 = '    vb.gui = ' + guiboolean
    newstring_3 = '    vb.memory = "' + str(memory) + '"\n    vb.cpus = "' + str(cpus) +'"'
    newstring_4 = '  end'
    newstring_5 = ' config.vm.provision "shell", inline: <<-SHELL'
    newstring_6 = '   echo -e "root\nroot" | sudo passwd && sudo su'
    if update_bool:
        newstring_7 = '   DEBIAN_FRONTEND=noninteractive apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get -y install && DEBIAN_FRONTEND=noninteractive apt-get autoremove -y && DEBIAN_FRONTEND=noninteractive apt-get autoclean -y'
    else:
        newstring_7 = '   echo "Welcome to your Virtual Kali Machine!"'
    newstring_8 = ' SHELL'

    ### Some fancy printouts for users
    print(20 * '-')
    print('Overwriting Vagrantfile.')
    print(20 * '-')
    print(".\n")
    t.sleep(0.1)
    print(".\n")
    t.sleep(0.1)
    print(".\n")
    t.sleep(0.1)

    ### Using the replace_string_in_file() function to configure the Vagrant file
    replace_string_in_file("vfileold.txt", "vfilenew.txt", oldstring_1, newstring_1)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_2, newstring_2)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_3, newstring_3)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_4, newstring_4)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_5, newstring_5)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_6, newstring_6)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_7, newstring_7)
    sh("cp vfilenew.txt tempfile")
    replace_string_in_file("tempfile", "vfilenew.txt", oldstring_8, newstring_8)


'''
Function for cleaning up temp files made for the process of replacing strings in the Vagrantfile
'''
def temp_files_cleanup():
    print(20 * '-')
    print('Cleaning up temporary files.')
    print(20 * '-')
    sh("rm -rf tempfile vfilenewcopy.txt vfileold.txt vfilenew.txt")

'''
Main function
'''
def main():
### Setting command for bringing up the machine and using the functions to overwrite the Vagrant file and configure it according to the user given parameters
    if arg.command == 'machineup' or arg.command == 'init':
        print("Hiya! Kali huh? so you're a hacker...\nLet me help you set up the machine to your personal preferences, But first we will let vagrant initialize the machine")
        print(20 * '-')
        if os.path.isfile('Vagrantfile'):
            remove_vagrantfile = input("You already have a Vagrant file in this directory, do you want us to remove it? (Y/n)")
            if remove_vagrantfile == 'Y' or remove_vagrantfile == 'y' or remove_vagrantfile == '':
                sh("rm -rf Vagrantfile")
                print("Now that that thing is gone, we can initialize the machine properly!")
                sh("vagrant init kalilinux/rolling")
            else:
                sys.exit()
        else:
            sh("vagrant init kalilinux/rolling")
        print(20 * '-')
        print('\n')
        print("Alright, now that that's over with, let us configure the machine together!")
        sh("touch tempfile")
        sh("cp Vagrantfile vfileold.txt")
        sh("cp Vagrantfile vfilenew.txt")
        overwrite_vagrantfile()
        sh("cp vfilenew.txt vfilenewcopy.txt")
        sh("rm -rf Vagrantfile")
        sh("mv vfilenew.txt Vagrantfile")
        temp_files_cleanup()
        sh("vagrant up")
        sh("vagrant ssh --command 'su'")
        sys.exit()
### Setting command for bringing down and destroying the machine and its related files
    elif arg.command == 'machinedown' or arg.command == 'destroy':
        sh("vagrant destroy")
        sh("rm -rf .vagrant Vagrantfile")
        sys.exit()
### If no valid command flag was given, inform the user of their mistake and print a helpful message
    else:
        print('That is not a valid command... maybe you made a typo?\nuse "python3 kalivm.py -h" to see available commands, or use "python3 kalivm.py -c machineup" to create a Kali machine!')
        sys.exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sh("rm -rf .vagrant Vagrantfile")
        print("\nYou interrupted the program with Ctrl+C")
        temp_files_cleanup()
        print("See ya next time!")
        try:
            sys.exit()
        except SystemExit:
            os._exit(1)

