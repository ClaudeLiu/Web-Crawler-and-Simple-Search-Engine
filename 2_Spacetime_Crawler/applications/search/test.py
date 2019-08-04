#a = ["www.google.com", "www.baidu.com"]
# b = ["a", "b", "c"]
# for x in a:
#     file.write(x)
# temp = file.readlines()
# print(temp)
##import os
##
##
##file = open("test.txt", "r")
##if os.stat("test.txt").st_size == 0:
##    print "success"
##
##for i in file:
##    print "python"
##    print i
##    binary = i.rstrip('\n').split(',')
##    print ("binary is: {}".format(binary))
##    if len(binary) == 0:
##        print "empty sadasd"
##        break
##    print (binary)
##    dict[binary[0]] = binary[1]
##    print "aaaa"
##    print(i.rstrip('\n'))

# print(dict)

#file.write("ccc")

# if "b" not in temp:
#     for i in b:
#         file = open("test.txt", "a")
#         file.write(i+"\n")

#file.close()

url = "https://today.uci.edu/event/from/personal/data/to/personal/health/tools/to/reduce/burden/and_improve_collaboration#.Wu5dGtMvzfY"
url_encode = str(url.encode("utf-8"))
slash_count = 0
for i in url_encode:
    if i == "/":
        print i
        slash_count += 1
    if slash_count > 12:
        print "yeah"







