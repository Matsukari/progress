#!/usr/bin/bash
echo "doc'ed"
read -p "read: " inp
echo $inp > ex.data

# expression: $((expr)); $(($a + $b)); or let varname=expr
# cond ex: [ $a -eq $b ]; deliberate spaces
# access evaluated prev cond: $?

# cond expr: 
#   [ -e filepath ] Returns true if file exists.
#   [ -x filepath ] Returns true if file exists and executable.
#   [ -S filepath ] Returns true if file exists and its a socket file.
#   [ expr1 -a expr2 ] Returns true if both the expression is true.
#   [ expr1 -o expr2 ] Returns true if either of the expression1 or 2 is true.
# 	[ -s filename ] True if the file exists and has a size greater than zero;
#	[ f1 -nt f2 ] True if f1 newer than f2
# 	[ f1 -ot f2 ] True if f1 older than f2
# -d dir, true if dir exist

# -z, true if string zero
# -n, true if not zero

# if [ cond ]; then
#	statement
# elif [ cond ]; then
#	statement
# else
#	statement
# fi


# function funname 
# {
#	definition
# }
# call args: $1, $2.....$n; either in shell or calling function

# call command or function: idname arg1 args...

# for varname in arrname; do
# 	definition
# done

# inside termina
#$ echo -e "\e[?1000h"
#$ while read -n 6; do echo hellowworld; done

#	import argparse

#	parser = argparse.ArgumentParser("simple_example")
#	parser.add_argument("counter", help="An integer will be increased by 1 and printed.", type=int)
#	args = parser.parse_args()
#	print(args.counter + 1)