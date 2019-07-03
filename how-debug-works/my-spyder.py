#!/usr/bin/env python
# Simple debugger
import sys
import readline

# Our buggy program
def remove_html_markup(s):
    tag   = False
    quote = False
    out   = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif c == '"' or c == "'" and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out
    
# main program that runs the buggy program
def main():
    print(remove_html_markup('xyz'))
    print(remove_html_markup('"<b>foo</b>"'))
    print(remove_html_markup("'<b>foo</b>'"))

# globals
breakpoints = {9: True}
stepping = False

def debug(command, my_locals):
    global stepping
    global breakpoints
    
    if command.find(' ') > 0:
        arg = command.split(' ')[1]
    else:
        arg = None

    if command.startswith('s'):     # step
        stepping = True
        return True
    elif command.startswith('c'):   # continue
        stepping = False
        return True
    elif command.startswith('p'):    # print 
        if arg:
            if arg in my_locals:
                print('{} = {}'.format(arg,repr(my_locals[arg])))
            else:
                print('No such variable: {}'.format(arg))

        else:
            print(my_locals)
    elif command.startswith('b'):
        if arg:
            breakpoints[arg] = True
        else:
            print("You must supply a line number")
    elif command.startswith('q'):   # quit
        sys.exit(0)
    else:
        print ("No such command", repr(command))
        
    return False

commands = ["b 5", "c", "c", "q"]

def input_command():
    #command = raw_input("(my-spyder) ")
    global commands
    command = commands.pop(0)
    return command

def traceit(frame, event, trace_arg):
    global stepping

    if event == 'line':
        if stepping or frame.f_lineno in breakpoints:
            resume = False
            while not resume:
                print (event, frame.f_lineno, frame.f_code.co_name, frame.f_locals)
                command = input_command()
                resume = debug(command, frame.f_locals)
    return traceit

# Using the tracer
sys.settrace(traceit)
main()
sys.settrace(None)
