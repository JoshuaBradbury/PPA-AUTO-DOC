# PPA AUTO-DOCUMENTATION TOOL

This tool is designed to aid in the creation of the PPA coursework documentations.

It will generate the pseudocode based on the actual code (However this version is based heavily on the formatting, like the right placement of spaces etc).

On top of this it will allow you to comment the code and will create separate files with the commented code, aptly named, and also put the commented code into a zip.

Other than automatically creating the Intro based on the comments about the files it will allow you to write the description, and save it between uses of the script so you don't have to write it each time.

The last thing it does is open up a tkinter window and allow you to organise the components of the diagram, so you can place them appropriately. To aid this it automatically snaps the arrow points to the closest free corners of the diagrams. Press Escape or close the window to finish editing the diagram and save it for use.

The command line options are like so:

test.py Coursework-No [write-comments] [write-class-diagrams] [write-description]

write comments, write class diagrams and write description are all either a "y" to allow you to write the comments, class diagrams or description, and a "n" if you want to use pre existing stuff, or you just don't want to do them yet.

Tools needed:

Bash - You should be running a bash based operating system because it runs some commands that are strictly for them.
PDFLatex - Also you should have pdflatex installed on the command line so it can generate the pdf.
Google Chrome - After it has finished it automatically displays the pdf in google chrome.


I've added my PPA 10 to show how it works with my code properly, I will also upload the java Auto Doc if you want to see how your code can be turned into pseudocode.
