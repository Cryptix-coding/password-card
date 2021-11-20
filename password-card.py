import secrets
from fpdf import FPDF, HTMLMixin


class PDF(FPDF, HTMLMixin):
    pass


document = PDF()
document.add_page()
document.set_font('helvetica', size=12)

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!()=?{[]}'  #all usable characters for the password card
head = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZß', '.!?']  #Entries of the first line of the password card


def random_string():
    return secrets.choice(alphabet) + secrets.choice(alphabet) + secrets.choice(alphabet)  #generates a random string of length 3


def generate_password_card():  #generates a random string of length 3
    pc = []  #container for the individual lines of the password card
    for row in range(10):  #line index from 0 to 10 since 10 lines in total
        row = []  #reset the line
        for col in range(10):  #Columns (entries in the rows list)
            row.append(random_string())
        pc.append(row)  #add the content to the password card
    return pc  #return the password list


def save_pc(filename, pc):
    to_save = ''  #string for the password
    for row in range(len(pc)):  #expire password list
        for col in range(len(pc)):
            to_save += pc[row][col]  #add the content of the variable
        if row != len(range(len(pc))) - 1:
            to_save += '\n'  #Line break as long as not at the end of the line (formatting)
    with open(filename, 'w') as out:
        out.write(to_save)  #Write the result to the file that was defined as the transfer parameter


def load_pc(filename):
    pc = []  #emty container for storing the password card
    with open(filename, 'r') as pc_in:  #open the file in read mode and go through the contents line by line
        for row in pc_in:
            row = row.strip()  #remove line breaks
            pc.append([row[0 + i:3 + i] for i in range(0, len(row), 3)])  #splitting the string into packets of 3. Results are written to a list and then added to the password map
    return pc


def generate_password(pc, keyword):
    password = "" #variable in which the password is
    rows = len(pc) #read out the number of lines in the password map
    for row in range(len(keyword)): #scroll through the lines of the password card as long as there are characters in the keyword
        for col in range(len(head)): #each line is now scrolled column by column and checks in which 3-packet the current letter of the sickword occurs
            if keyword[row] in head[col]: #If the letter was found in a column
                password += pc[row % rows][col] #add the 3's packet at the corresponding position to the password; calculate the line index % of the number of lines to make sure that after 10 digits you start from the top again
                break
    return password


def write_pdf():  #Method to create PDF password card
    pc = load_pc("password_card.txt")
    #print(pc)
    width = int(100 / (float(len(head)) + 1.0))
    html_table = '<h1>Password Card</h1>\n<table border="1"><thead>\n<tr>\n'
    html_table += '<th width="' + str(width) + '%"> Counter </th>\n'
    for th in head:
        html_table += '<th width="' + str(width) + '%">' + th + '</th>\n'
    html_table += '</tr>\n</thead><tbody>'
    i = 1
    for row in range(len(pc)):
        if i % 2:
            html_table += '<tr bgcolor=#22FF22">'
        else:
            html_table += '<tr bgcolor=#DDFFDD">'
        html_table += '<td>' + str(i) + '</td>\n'
        i += 1
        for col in range(len(pc)):
            html_table += '<td>' + pc[row][col] + '</td>\n'
        html_table += '</tr>'
    html_table += '</tbody></table>'

    #print(html_table)

    document.write_html(html_table)

    document.output("Password_card.pdf")  #save the PDF


#--------------------------------------------------


#generating Password-card .txt and .pdf
def make():
    save_pc("password_card.txt", generate_password_card())  #generate the password map and save it as a .txt file
    write_pdf()  #create the PDF

#controlling
g = 0
generate = input("If you have already a password-card you want to use, press (n). If you don't have one press (y).\r\n"
                 "Do you want to generate a password card (y/n)? ")
if generate == "y":
    g = 1

keyword = input("keyword (capital letters): ") #Word from which the password will be created (May only contain uppercase letters)
if g == 1:
    make()
print("-------------------- \r\n")
generated_passwort = generate_password(load_pc("password_card.txt"), keyword) #generates a password from the given word
print("Your password is: " + generated_passwort)
print("Your reminding sentence is: " + keyword)