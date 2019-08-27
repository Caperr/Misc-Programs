#TODO:
#- FINISH WRITING SENT EMAILS
#- !!!EXTEND STORYLINE!!! ADD ACCOUNT TO MAIN SERVER, FELICIA. SOMETHING CAT RELATED AS PASSWORD
#- ADD EMAILS TO JEFFS INBOX AND SENTBOX RELATIVE TO STORYLINE ABOVE ^^^^
#- ADD MORE EMPLOYEES TO EMPLOYEES DATABASE
#- ADD MORE FIELDS TO EMPLOYEES DATABASE I.E DOB, DATE OF EMPLOYMENT??
#- CONVERT DATABASE DOCUMENT INTO AN ARRAY... MAYBE. USE TO REPLACE 'ADDRESSES' VARIABLE? MAYBE KEEP IT AND JUST CREATE A WHOLE NEW VARIABLE FOR ALL CHARACTERS AND THEIR DETAILS???? IDK
#- GO THROUGH CODE AND DO COMMENTING, SPACING, MAKE WHAT'S PRINTED TO COMMANDLINE PRETTIER
#- ADD FLATFILE GAME SAVES LIKE IN TEXT RPG - ASK FOR PLAYER NAME AT START AND BASE THEIR LOCAL SHELL NAME AND EMAIL ADDRESS OFF OF IT: VARIABLE 'NAME' IS ALREADY CREATED
#- UPDATE 'EXIT' COMMAND TO SUPPORT CUSTOM NAMES ^^^
#- FINISH SCP - TIDY UP AND ADD FACT (FOR REAL SYNTAX)
#- TIDY EMAIL INBOX AND SENTBOXES INTO TABLES. WHEN PRINTING THE TABLE, USE THE LENGTH OF THE VARIABLES TO DECIDE HOW MANY SPACES TO ADD
#- COME UP WITH MORE EFFICIENT WAY FOR RECIEVING TIPS - I.E EINBOX AND EOPEN. MERGE TIP VARIABLE WITH EMAILS VARIABLE, AND ADD A NEW VALUE TO DETERMINE IF IT'S A NORMAL EMAIL OR A TIP???? MAYBE?????
#- ADD DATE TO TOP OF SHELL?
#- FIX UP DATES IN EMAILS, SENTS AND TIPS. HAVE IT BASED OFF OF THE DATE IN SHELL.
#- FIND MORE EFFICIENT WAY TO DO GETMAIL FUNCTION XD
#- TWEAK EMAIL WRITING SPEEDS
#- MAKE IT POSSIBLE FOR FILES TO HAVE PASSWORD PROTECTION
#- MOVE SCPCOUNT VARIABLE INTO TIPS AND CHANGE THE WAY IT IS CALLED IN SCP COMMAND
#- CHANGE EMAIL SEND. YOU CAN CURRENTLY EMAIL CLIENT456 FROM ANY ADDRESS (E.G JEFF)
#- ADD GETMAIL COMMAND TO EMAIL CLIENT SO YOU DONT HAVE TO LEAVE IT TO GET NEW TIP EMAILS
#- ADD USER SENT EMAILS TO THE SENT EMAILS ARRAYS SO THEY CAN BE READ WITH 'SENT' COMMAND

#HACK()
#A game to teach the user some rudimentary BASH commands. Written by Jasper Law.

#Import support libraries
import time

#===========VARIABLE DECLARATION==============

#This first array stores all of the available servers, their addresses, their server
#ID (called 'place'), and all of the users and their passwords for that server.
#The array is in the format:
#[
#    [server,
#        place,[[name,pw],[name,pw]],servername,level           'level' means the level associated with that server. (what level you are elevated to
#    ],                                                         when you access that server)
#    [server,                                                   This could easily be done by just getting the server array's position in the main
#        place,[[name,pw],[name,pw]],servername,level           svrs array... Oh well, this is more convenient.
#    ]
#]
svrs = [
    ['localhost',
        1,[['']],'localhost',1],

    ['192.168.0.5',
        2,[['guest']],'Local-Server',2],

    ['97.73.9.646',
        3,[['jeff','password']],'Clients-Server',3],

    ['12.89.5.309',
        4,[['jeff','04/11/1958'],['felicia','sooty']],'Main-Server',4],

    ['77.15.3.636',
        5,[['felicia','sooty']],'Research-Development',5]
]

#The server ID. Used to decide which server the user is currently connected to.
place = 1

#This variable is used to store the address of the server the user is connected to.
#Not needed in any way, but I use it to print the address when calling exit
#for more realism.
svr = ''

#Used for copying the details of the current server, taken from the 'svrs' array.
#The user starts in 'localhost', so set it to 0 by default.
svraddr = svrs[0]

#For counting the number of times atip was called
tips = 0

#For limiting the number of times cheat and can be called
cheats = 3

#This is for tracking whether or not the user has recieved a new email alert
emailcount = False

#A variable to track whether or not the user has seen this tip.
scpcount = False

#Later used for storing the currently active email address
emailaddr = ''

#An array holding all of the emails in the game. Format is:
#[                                                                                  open the array
#   [email address,                                                                 the user with address email address has
#       [                                                                           these emails
#           [email name, email, level requirement,sent from, date,read],                 the first has name email name, contents email, a level requirement, is from this address, and was sent on this date. Has it been read?
#           [email name, email, level requirement,sent from, date,read]                  the following emails have the same list of values
#       ]                                                                           end the email list
#   ],                                                                              end the email list under that address
#                                                                                   (and the same again...)
#   [email address,                                                                 the user with address email address has
#       [                                                                           these emails
#           [email name, email, level requirement,sent from, date,read],                 the first has name email name, contents email, a level requirement, is from this address, and was sent on this date. Has it been read?
#           [email name, email, level requirement,sent from, date,read]                  the following emails have the same list of values
#       ]                                                                           end the email list
#   ],                                                                              end the email list under that address
#   ],                                                                              end the document list under that user name
#]
emails = [
    ['deeperresearch@gmail.com',
        [
            ['A friendly request',"""Dear DeeperResearch,
Recently I stumbled across a rather interesting piece of news. The company I once worked for
will soon be releasing a new 'wonder drug', which they claim to completely cure irrational fears.
For reasons I cannot explain to you at this point, I need you to investigate further.
I heard about you from a friend of mine who also used your... 'research' services. I can tell
you that if we uncover evidence of my theory, your reward will be great.
The company is called BioInnovations.

To start off, I've set up a file server containing the addresses of several other servers.
It should be accessible on your local area network at 192.168.0.5. For now only the guest
account will be available to you, but that may change as you progress...
To begin the hack, SSH into the server 192.168.0.5 with username guest.

Good luck.
- A friend

P.S You can email me at any time if you'd like a bit of help.""",1,'client456@gmail.com','12/02/15',False]
            ]
    ],

    ['JeffSmith@gmail.com',
        [
            ['Re: Welcome to BioInnovations',"""Dear Mr. Smith,
    Gemma has just informed me that your phone was stolen yesterday afternoon, how inconvenient. However, it should be covered
by the insurance that comes with your job. Since you've lost your phone, you shan't be able to retrieve the address of the
main server. So, the main server's address is 12.89.5.309
Again, please change your password as soon as you gain access. As you know, the boss is not willing to take any risks at this stage.

Please reply to this message if you encounter any problems.
- J Turner, Senior Management""",3,"J.Turner@BioInnovations.org","11/02/2015",False],

            ['Welcome to BioInnovations',"""Dear Mr. Smith,
    Congratulations on getting this job, I understand you've been applying for quite some time now. How very
fortunate for you that our previous clients manager became unavailable to us.
For convenience, please add your personal details to our employees database. The database is
stored on the main server, and if i'm not mistaken, I sent the address to your phone. Your username
should be the same, and the password has been set to the date of birth of our latest client, Mr. A Johnstone.
Please change your password *as soon as possible*. We cannot risk any security vulnerabilities at this
stage in our development.

I look forward to working with you.
- J. Turner, Senior Management""",3,"J.Turner@BioInnovations.org",'10/02/2015',True]
        ],
    ],

    ['1CherryF@Gmail.com',
       [
            ["Jeff Smith Interview", """Hi again Felicia,
    Just thought I should let you know that the interview went smoothly,
and we're all content. Mr Smith will start his first day on the 12th.

Thanks,
John""", 4,"JTurner-SM@BioInnovations.org", "09/02/2015",True],

           ["Re: New Clients Manager", """Hi Felicia,
    Actually yes, there is an opening... Unfortunately I wasn't informed as to
why the last clients manager became unavailable to us, but there it is.
Haha, that's fair enough. I suppose it's time we gave him a break. I'll arrange an
interview for the 8th.

All the best,
John""", 4,"JTurner-SM@BioInnovations.org", '05/02/2015',True]
        ]
    ],
    ['client456@gmail.com',
        [
        ]
    ],
    ['JTurner-SM@BioInnovations.org',
        [
        ]
    ]
]

#A second email database, for sent emails. Same format as above but with address sent to rather than from. Also, 'read' is no longer necessary.
sent = [
    ['JeffSmith@gmail.com',
        [
            ['Re: Job help',"""Hey Cherry,
    Thanks again for landing me this job, really need the money right now. How are the cats? Special love to Sooty
from me <3

Fancy a drink some time?
Jeff x""",3,"1CherryF@Gmail.com",'11/02/2015']
        ]
    ],

    ['1CherryF@Gmail.com',
        [
            ['New Clients Manager',"""Hi John,
    I heard from Gid'on that there was an opening in clients management, what happened to the last guy?
I was thinking, isn't it about time we gave Jeff Smith an interview? He's been trying to
get a job here for more than a year now...

Think about it.
Felicia""",4,"JTurner-SM@BioInnovations.org",'05/02/2015']
        ]
    ]
]

#Yet another email database, dedicated to tips from the client. The format is:
#[
#   [tip name, tip, level, mailed, read],      #'mailed' is just whether or not the tip has been mailed to the user.
#   [tip name, tip, level, mailed, read]       #obviously the game will change this value as appropriate.
#]
tip = [
    ['Re: A friendly request',"""Hello,
I have a fair bit of experience in... Data retrieval myself. Anyway, about the task.
The first thing I need you to do is ssh into a server with the username guest and address 192.168.0.5

If you've never used ssh before, here's the syntax: ssh <username>@<address>
In other words, you need to run the command ssh guest@192.168.0.5

Tell me if you need anything else.""",1,False,False],
    ['Re: Level two tip',"""Hi again,
There's a file on this drive with the first server address, find it using ls, and open with cat. Use the help
command if you need more info.

Also, you may get the following error whilst SSHing into the next server:
"Permission denied (publickey,password,keyboard-interactive)."
The error means you've put in an incorrect password too many times and will need to reopen the connection.

Good luck.""",2,False, False],
    ['Re: Tip for level three',"""Hello,

You're doing great so far. Now, Since Jeff only works in client management,
he doesn't have very much access to the system. So, let's try and get into a server with more accounts.

Unfortunately, there doesn't seem to be any useful files on the drive... Maybe there'll be some clues in
Jeff's email account?

Let me know how it goes.

PS: The email software installed on your system appears to be slightly different to that of the real shell.
If you want to know how to access email from the real shell, read this fedoraproject post: http://is.gd/oZ2sFo""",3,False,False],
    ['Re: Tip for level four',"""Hello,

Hm. This server is a lot more bare than i was expecting. However, that employees database could be useful
for finding a new login. If Jeff doesn't have access, look into downloading it with scp.
I doubt that database will have any password info, so you're on your own there. Snoop around a bit more in
Jeff's emails, maybe check his sent emails too.

I'll be awaiting your reply.""",4,False,False]
]
#    ['Re: Re: Tip for level four',"""Hi,
#
#Ok, I've obtained """,4,False,False

#this one is for all of the emails the player will send throughout the game. The extra value is whether or not it has been sent.
send = [
    ['deeperresearch@gmail.com',
        [
            ['Re: A friendly request',"""Hello,
Let me get this straight, you hacked into my local network and installed a separate file server?
How?
Now, could you please explain the task again? It doesn't really make much sense.

Best,
Deeperresearch""",1,"client456@Gmail.com", False],
            ['Level 2 tip',"""Hi,
I've got access to the file server. This isn't half bad, either...
Now, what do you want me to do from here? I still haven't even got access to the BioInnovations servers.

Best,
Deeperresearch""",2,'client456@Gmail.com',False],
            ['Tip for level three',"""Hi client,
Looks like your information is reliable, I'm in.
I'm new to this server system, so can you explain where to go next?

Thanks,
Deeperresearch""",3,'client456@Gmail.com',False],
            ['Tip for level four',"""Hi again client,
I got into the main server. Unbelievable how careless this Jeff guy is.
Anyway, I don't have any more login credentials as of yet. Any ideas where to get some?

Thanks,
Deeperresearch""",4,'client456@Gmail.com',False]
        ]
    ],

    ['1CherryF@Gmail.com',
        [
            ['R&D Server IP',"""Hi there John,
    Really sorry, but I've misplaced the IP for the R&D department's data server...
What was it again?

Thanks muchly,
Felicia

PS. I'd appreciate it if you didn't mention this to anyone, I'm getting known
around the department as the forgetful bimbo.""",4,"JTurner-SM@BioInnovations.org", False]
            ]
     ]
]

#One last email variable, it stores the emails sent by npcs, that are not originally sent.
#[[receiver,[....
npcsend = [
    ['1CherryF@Gmail.com',
        [
            ['Re: R&D Server IP',"""Hi,
    You? Forgetful? Hah!
The IP is 77.15.3.636. And don't worry, I'll keep this between us.

Best,
John""",1,"J.Turner@BioInnovations.org", False]
        ]
    ]
]

#This variable stores all of the email addresses and what user names they are associated with.
#The array is in the format:
#[
#    [username, address],
#    [username, address],
#    [username, address]
#]
addresses = [
    ["jeff","JeffSmith@gmail.com"],
    ["anonymous","deeperresearch@gmail.com"],
    ['client',"client456@gmail.com"],
    ["felicia","1CherryF@Gmail.com"]
]

#For counting the number of facts found by the user
points = 0

#For storing the user's progress through the game
level = 1

#For storing all of the game's 'fun facts', and whether or not the fact has been displayed.
#The array is in the format:
#[
#    [fact, displayed, fact number],        'displayed' is whether or not the fact has been displayed yet
#    [fact, displayed, fact number],        'fact number' is simply the number of the fact in relation to the list
#    [fact, displayed, fact number]
#]
facts = [
        ["""\nFACT #1: BASH stands for Bourne Again SHell, as Bourne is the name of the inventor of the
original shell, and this is his second work.""",1,1],

        ["""FACT #2: SSH stands for Secure SHell, or sometimes Secure Socket sHell.
SSHing is for accessing the files on one computer or server from another,
which can be very useful in businesses which require the same files in two
different locations. Not only can SSH access files, but it can also be used to
send commands to remotely control servers or devices. How very convenient!""",1,2],

        ["""\nFACT #3: Args is short for arguments. That is the name of any extra information you
give a command when calling it. For example, if i were to call the command 'cat file.txt', 'cat'
is the command and 'file.txt' is the argument. Of course, some commands take multiple arguments,
and some dont take any at all. However, you can't just use any old argument, it has to be
valid, in other words, from the list of arguments compatible with that command. Another example,
I can't call 'cat hello', because 'hello' is not a file or web page.
This principle is the same for any kind of language, be it programming or scripting, or anything else really!\n""",1,3],

        ["""\n FACT #4: Syntax means the way you say a command. For example, when you order some food
at a restaurant, you would say "Can I have this please?", not "This have I please can?". It works the
exact same way with commands in programming. When you ask the system to open a file, you say "cat file.txt"
rather than "file.txt cat". The unfortunate part of syntaxes is the fact that the system cannot understand
pure English, meaning we can't type things like "Can you show me the file file.txt please?". However, when you
think about it, they are essentially the same thing but stripped down a bit.\n""",1,4]

]

#The user's name
name = 'anonymous'

#For storing what name the user is connected to a server under
user = 'anonymous'

#What to print to command line when taking input
username = 'anonymous$'

#An array holding all of the documents in the game. Format is:
#[                                                                                  open the array
#   [user name,                                                                     the user with name user name has
#       [                                                                           these documents
#           [document name, document, level requirement, place requirement, home, [user, user, user]],  the first has name document name, contents document, a level requirement,
                                                                                    #and a place requirement. NEW: Do you need to be out of SSH to read? NEW: Usernames requirement
#           [document name, document, level requirement, place requirement, home, [user, user, user]]   the following documents have the same list of values
#       ]                                                                           end the document list
#   ],                                                                              end the document list under that user name
#                                                                                   (and the same again...)
#   [user name,                                                                     the user with name user name has
#       [                                                                           these documents
#           [document name, document, level requirement, place requirement, home, [user, user, user]],  the first has name document name, contents document, a level requirement,
                                                                                    #and a place requirement. NEW: Do you need to be out of SSH to read? NEW: Usernames requirement
#           [document name, document, level requirement, place requirement, home, [user, user, user]]   the following documents has the same list of values
#       ]                                                                           end the document list
#   ],                                                                              end the document list under that user name
#]                                                                                  close the array.

#Where user name is 'none', the document can be accessed from any account.
docs = [
    ['none',
        [
##            ['task.txt',"""Welcome to HACK()! This game is an attempt to teach the user some basic
##BASH knowledge while at the same time hacking into a major cooperation. Two Birds, one stone!
##ALL of the commands (unless specified) used in this game are real BASH commands!
##In other words, right now, you're learning a scripting language! Easier than you'd expect, isn't it?
##Along the way, I'll also provide you with some interesting facts about the stuff you're using.
##Don't worry, to make them as bearable as possible, you'll only see these facts once each.
##
##Recently I stumbled across a rather interesting piece of news. The company I once worked for
##will soon be releasing a new 'wonder drug', which they claim to completely cure irrational fears.
##For reasons I cannot explain to you at this point, I need you to investigate further.
##I heard about you from a friend of mine who also used your... 'research' services. I can tell
##you that if we uncover evidence of my theory, your reward will be great.
##The company is called BioInnovations.
##
##To start off, I've set up a file server containing the addresses of several other servers.
##It should be accessable on your local area network at 192.168.0.5. For now only the guest
##account will be available to you, but that may change as you progress...
##To begin the hack, SSH into the server 192.168.0.5 with username guest.
##Good luck!""",1,1, False, []],

            ['recent_transactions.txt',"""CLIENT NAME:ANDREW JOHNSTONE
- 06/01/2015:£300:OUTGOING
- 22/11/2014:£50:OUTGOING
- 14/11/2014:£670:INCOMING
- 26/06/2014:£530:INCOMING
- 07/05/2014:£120:OUTGOING

CLIENT NAME: MARK PETERS
- 20/12/2014:£490:OUTGOING
- 11/07/2014:£70:OUTGOING
- 30/04/2014:£150:INCOMING
- 28/02/2014:£630:INCOMING
- 28/01/2014:£210:OUTGOING

CLIENT NAME: G. PANiK
^¥©ƒ´˚ß >>>SKIPPING OVER CORRUPT DATA<<< ˙ø^¥å©˙ß˚˙©

CLIENT NAME: DAVID CARLSON
- 01/02/2015:£610:INCOMING
- 11/11/2014:£350:OUTGOING
- 02/10/2014:£680:INCOMING
- 18/08/2014:£450:OUTGOING
- 03/05/2014:£370:INCOMING

CLIENT NAME: COLIN STEVENS
- 03/02/2015:£630:OUTGOING
- 29/01/2015:£210:OUTGOING
- 24/01/2015:£40:OUTGOING
- 14/01/2015:£610:OUTGOING
- 27/12/2014:£680:OUTGOING

CLIENT NAME: THOMAS LEE
- 01/02/2015:£580:OUTGOING
- 22/01/2015:£240:OUTGOING
- 10/01/2015:£260:OUTGOING
- 05/01/2015:£330:OUTGOING
- 02/01/2015:£530:OUTGOING""",6,3, False,[]],

            ["employee_profiles.db","""=STAFF CURRENTLY IN EMPLOYMENT=
NAME                |JOB TITLE          |SALARY     |EMAIL
--------------------|-------------------|-----------|-----------------------
SUSAN RODNEY        |PUBLIC RELATIONS   |£36,730    |S.RODNEY@HOTMAIL.COM
GOSTISLAV ROSSINI   |PUBLIC RELATIONS   |£36,730    |ROSSINIG@HOTMAIL.COM
THOMAS BROWN        |R&D                |£67,000    |TOMMYB23@HOTMAIL.COM
MATTHEW TOP         |R&D                |£67,000    |MATTHEWTOP4@LIVE.COM
GEMMA BROWN         |RECEPTION          |£44,500    |GEMMABROWN22@HOTMAIL.COM
FELICIA CHERRY      |R&D                |£67,000    |1CHERRYF@GMAIL.COM
KEVIN STEVENS       |RESOURCE MANAGEMENT|£74,000    |KEVIN.STEVENS@LIVE.COM
LAVINIA MOLLOWN     |RECEPTION          |£45,000    |LAVINIAMOLLO@GMAIL.COM
OTMAR VIRTANEN      |VICE PRESIDENT     |£144,250   |O.VIRTANEN@BIOINNOVATIONS.ORG
JULIJANA LONGO      |COMMUNICATIONS     |£66,100    |JULIANA.L9@HOTMAIL.COM
JOHN TURNER         |SENIOR MANAGEMENT  |£88,000    |J.TURNER@BIOINNOVATIONS.ORG
GID'ON MALLEY       |HEAD OF R&D        |£77,000    |MALLYMAN123@GMAIL.COM
DOLORES PETERS      |TECH SUPPORT       |£74,300    |PETERSDOLORES@GMAIL.COM
JEFFREY SMITH       |CLIENT MANAGEMENT  |£47,500    |JEFFSMITH@GMAIL.COM
TEODORA FRANJIC     |DATA ANALYSIS      |£75,000    |T.FRANJIC@BIOINNOVATIONS.ORG
BRYN TEKE           |TECH SUPPORT       |£74,300    |BRYNWITHAB@LIVE.COM
GERHARD GAGNIER     |MEDIA & ADVERTISING|£55,000    |G3RHARDG4GNIER@LIVE.COM
TYTUS SORENSEN      |MEDIA & ADVERTISING|£55,000    |TYTUS.SORENSEN@GMAIL.COM
PHOEBE NAZARIO      |HEAD OF MEDIA      |£60,500    |P.NAZARIO@BIOINNOVATIONS.ORG
G. PANiK            |IMPORTS            |NOT ON FILE|UNKNOWN
AINSLEY LANTOS      |CEO                |£255,646   |A.LANTOS@BIOINNOVATIONS.ORG
DENIYAH TOSELLI     |CLEANER            |£35,050    |DENIYAHTOSELLI@GMAIL.COM
MARIAN VELAZQUEZ    |CLEANER            |£35,050    |M.VELAZQUEZ@GMAIL.COM
""",4,4, True, ['PANiK','felicia']]
        ]
    ],

    ['guest',
        [
            ['location1.txt',"""This first server is the one that this company uses simply to store a list
of all of their clients, and nothing else. There are only a few registered users, but I think you will
find that their new employee, Jeff, has not yet changed his password from the default... The server's
IP address is: 97.73.9.646 You can drop me an email if you get stuck.""",2,2, False, ['guest']]
        ]
    ],

    ['jeff',
        [
            ['client_profiles.txt',"""CLIENT NAME: ANDREW JOHNSTONE
CLIENT DOB: 04/11/1958
MOST RECENT TRANSACTION: 06/01/2015
SERVICE: NETWORK SECURITY
RELATIONSHIP: 7/10

CLIENT NAME: MARK PETERS
CLIENT DOB: 16/05/1951
MOST RECENT TRANSACTION: 20/12/2014
SERVICE: DELIVERIES
RELATIONSHIP: 5/10

CLIENT NAME: G. PANiK
CLIENT DOB: NOT ON FILE
MOST RECENT TRANSACTION: 15/02/2015
SERVICE: NOT ON FILE
RELATIONSHIP: 9/10

CLIENT NAME: DAVID CARLSON
CLIENT DOB: 13/08/1949
MOST RECENT TRANSACTION: 01/02/2015
SERVICE: PUBLIC RETAIL
RELATIONSHIP: 7/10

CLIENT NAME: COLIN STEVENS
CLIENT DOB: 20/02/1954
MOST RECENT TRANSACTION: 03/02/2015
SERVICE: RESEARCH & DEVELOPMENT
RELATIONSHIP: 10/10

CLIENT NAME: THOMAS LEE
CLIENT DOB: 25/07/1981
MOST RECENT TRANSACTION: 01/02/2015
SERVICE: CHEMICAL RETAIL
RELATIONSHIP: 8/10""",3,3, False, ['jeff']]
        ]
    ]
]

#This stores the messages that are to be printed upon level completion.
#The array is in the format:
#[
#    [message, level],
#    [message, level],
#    [message, level]
#]
lvlmsg = [
    ["You hacked into a file server on your LAN!",1],
    ["You hacked into the first external file server!",2],
    ["You hacked into the company's main server! This is where things get difficult...",3],
    ["You hacked into the R&D division's server!",4]
]


#=============FUNCTION DECLARATION=============


#Used to test if a value is int or not
def isnum(x):
    try:
        x = int(x)
    except ValueError:
        return False
    return True

def checkrequire(command,option1,option2):
    global level
    if command == 'esend':
        global emails
        global send
        if option1 == 'Re: A friendly request':
            if emails[0][1][0][5] == True and level == send[0][1][0][2]:
                return True
            else:
                return False
        if option1 == 'Level 2 tip':
            if level == send[0][1][1][2]:
                return True
            else:
                return False
        if option1 == 'Tip for level 3':
            if level == send[0][1][2][2]:
                return True
            else:
                return False
        if option1 == 'Tip for level 4':
            if level == send[0][1][3][2]:
                return True
            else:
                return False
        if option1 == 'R&D Server IP':
            if level == send[1][1][0][2]:
                return True
            else:
                return False
    return True

def getmail():
    global send
    global tip
    global npcsend
    global emails

    if level == 4 and send[1][1][0][4] and not npcsend[0][1][0][4]:
        emails[2][1].append([npcsend[0][1][0][0],npcsend[0][1][0][1],npcsend[0][1][0][2],npcsend[0][1][0][3],'11/02/15',False])
        npcsend[0][1][0][4] = True

    if tip[0][3] == False and send[0][1][0][4] == True:
        tip[0][3] = True
    elif tip[1][3] == False and send[0][1][1][4] == True:
        tip[1][3] = True
    elif tip[2][3] == False and send[0][1][2][4] == True:
        tip[2][3] = True
    elif tip[3][3] == False and send[0][1][3][4] == True:
        tip[3][3] = True
    # elif tip[4][3] == False and send





#Used to decide if a tip has been displayed or not, and print one if not.
#The 'x' variable is whether the tip has been displayed, i.e one of the values
#from the 'times' array
def printfact(id):
    global points
    global facts
    for i in range(len(facts)):
        if facts[i][2] == id and facts[i][1] == 1:
            print(facts[i][0])
            points += 1
            facts[i][1] = 0

#Used to display available commands to the user
def help():
    global place
    global user #Will later be used to give different usernames access to different commands, e.g changing other users' permissions.
    #These commands are available on ever server
    print("- help == display a list of available commands")
    print("- ls == list files in the current directory")
    print("- cat <file> == opens text files")
    print("- ssh <username>@<address> == SSH into a server using IP <address> and user <username>")
    print("- email == launch the email client*")
    #Depending on which server the user is connected to, additional commands are printed.
    #THIS COMMAND IS FOR LATER IN THE GAME
##    if place == 1:
##        print("- su == restart the shell under a different username")
    if place > 1:
        print("- exit == disconnect from the current SSH server")
        if level > 3:
            print("- scp <file> == download a file to your local drive")
    if level > 1:
        print("- cheat == get the solution to your current level*")
    print("\n*Not a real bash command")



#List the files available on the current server
def ls():
    tempcount = 1
    success = 0
    hasperm = False
    global place
    #User will be used later in the game for logging
    #into the same server as different users, to see different
    #sets of files/emails etc.
    global user
    global level
    #SECTION ONE
    #Reads all files for public files
    #Read from the docs array, for however many users are inside of it
    for i in range(len(docs)):
        #If the list of documents does not require a name
        if docs[i][0] == "none":
            #Read through the document list, for however many documents are listed
            for j in range(len(docs[i][1])):
                #If you have the required place
                if docs[i][1][j][3] == place:
                    if tempcount == 1:
                        print("=Public Files=")
                        tempcount = 0
                    #If the 'user' array is empty, it must be a public file, so they must have permission to open it.
                    if len(docs[i][1][j][5]) == 0:
                        hasperm = True
                    #If the user's user name appears in the users list, they must have permission to open the file.
                    else:
                        for k in range(len(docs[i][1][j][5])):
                            if user == docs[i][1][j][5][k]:
                                hasperm = True
                                break
                    #If the user's level is too low, or they aren't on the allowed users list, display a warning marker.
                    if docs[i][1][j][2] > level or hasperm == False:
                         print(" -", docs[i][1][j][0],"[!]")
                    else:
                        print(" -", docs[i][1][j][0])
                    success = 1

    if success == 1:
        print()

    #SECTION TWO
    #Reads through files only available to current user
    tempcount = 1
    for i in range(len(docs)):
        #If the list of documents' name is the same as your name
        if docs[i][0] == user:
            #Read through the document list, for however many documents are listed
            for j in range(len(docs[i][1])):
                #If you have the required place
                if docs[i][1][j][3] == place:
                    if tempcount == 1:
                        print("=Private Files=")
                        tempcount = 0
                    #If your level is too low, display a warning marker. This will be used later when we change users' access perms.
                    if docs[i][1][j][2] > level:
                         print(" -", docs[i][1][j][0],"[!]")
                    else:
                        print(" -", docs[i][1][j][0])
                    success = 1
    if success == 0:
        print("ERR: No files found")


#Used for opening files. Right now it is only used for text files, but i may
#add more functionality later in the game.
def cat(file):
    global place
    global user
    global level
    #Used to track whether or not the file was found
    success = 0
    #Same basic idea as the ls() command.
    #Read from the docs array, for however many users are inside of it
    for i in range(len(docs)):
        #If the list of documents does not require a name or is the same as your name
        if docs[i][0] == "none" or docs[i][0] == user:
            #Read through the document list, for however many documents are listed
            for j in range(len(docs[i][1])):
                hasperm = False
                #If the 'user' array is empty, it must be a public file, so they must have permission to open it.
                if docs[i][1][j][5] == []:
                    hasperm = True
                #If the user's user name appears in the users list, they must have permission to open the file.
                else:
                    for k in range(len(docs[i][1][j][5])):
                        if user == docs[i][1][j][5][k]:
                            hasperm = True
                            break
                #If you have the required place and level, the file matches your search, and you are on the allowed users list, print the document and set success to 1
                if docs[i][1][j][3] == place and docs[i][1][j][0] == file:
                    if docs[i][1][j][2] <= level and hasperm == True:
                        print(docs[i][1][j][1])
                    else:
                        print("ERR: ACCESS DENIED")
                    success = 1
    #If the open was not a success, an incorrect file name must have been requested. Print an error message
    if success == 0:
        print("ERR: The file",file,"does not exist.")
    elif success == 1:
        printfact(1)


#Connect to different servers via the SSH protocol. Of course, this and all
#of the servers used in the game are fake.
def ssh(login,address):
    success = ''
    if address == 'localhost':
        print("You can't SSH your own computer!")
        return
    global place
    if place != 1:
        print("SSH can only be performed from your local computer")
    else:
        global svraddr
        global level
        global points
        global svr
        global user
        global username
        global svrs
        #Set the value of 'svr' to the server address you are connecting to,
        #this will printed on call of exit
        svr = address
        #Used to track whether the user you are logging in as exists
        validu = 0
        #Used to track whether the server you are connecting to exists
        valids = 0
        #Used to track whether the SSH was a success
        success = 1

        #Remember, 'svrs' was my array containing all of the servers and their data.
        for a in range(len(svrs)):
            #Cycle through the list, checking each address value in the array against
            #the one you are connecting to
            if address == svrs[a][0]:
                #If the address is found in the array, set the valid server tracker to 1,
                #make a note of the location in the array of that address, and exit the loop
                svraddr = svrs[a]
                valids = 1
                break

        #If the server was not found in the array, say so. Then set 'success' to 0
        #to later indicate to the program not to complete the SSH.
        if valids == 0:
            print('server not found')
            success = 0

        #Do the exact same thing, but check against the users on the server.
        #Only do this if the server was found.
        if success == 1:
            for b in range(len(svraddr[2])):
                if login == svraddr[2][b][0]:
                    validu = 1
                    break
            if validu == 0:
                print('user not found')
                success = 0

        #This variable is just for convenience (it isn't necessarily needed, I could
        #instead just put svrs[a][2] or svraddr[2][b] when I need to access uP). It stores
        #the username and password of the user you are trying to log in as.
        if success == 1:
            uP = svraddr[2][b]

        #If everything is correct, simulate a connection!
        if success == 1:
            #Yeah, I know this isn't how SSH'ing normally looks in bash. Oh well.
            print('Accessing', end='')
            for c in range(3):
                print('.', end='')
                time.sleep(1)
            time.sleep(1)

            #To decide whether or not the requested account has a password, I check if the
            #variable exists. The username and password are stored in an array,
            #So i check if that array is 2 in length; Which means it will contain both a name
            #and password.
            if len(uP) == 2:
                #Request password from user
                pw = input("\n" + login + "@" + address + "'s password: ")

                for c in range(2):
                    #Check it, and give the user 2 extra chances if it's wrong.
                    if pw != uP[1]:
                        print("Permission denied, please try again.")
                        pw = input(login + "@" + address + "'s password: ")

                #If they didn't get it, return an error and set the success variable to 0.
                if pw != uP[1]:
                    print('Permission denied (publickey,password,keyboard-interactive).')
                    success = 0

            #If success is still 1..
            if success == 1:
                print("\nSSH successful.")
                #Set the place variable, taken from within the array.
                place = svraddr[1]

                #If you're connecting to a server and your level is less than
                #Its relative level, set it. Also, give congratulations upon level elevation.
                if level < svraddr[4]:
                    for d in range(svraddr[4] - level):
                        print("\n==========\nLEVEL",(level + d),"COMPLETE\n" + lvlmsg[level + d - 1][0] + "\n==========\n")
                    level = svraddr[4]
                    #print(level)

                #Set the username to the one that you logged in with, and add the
                #symbol used in SSH. (a #)
                user = login
                username = login + '#'
                #Update the email message tracker, in case of new emails
                emailcount = False

                #If the user hasn't SSH'd before, show a fact
                printfact(2)
    #Make sure the svraddr variable is the default if the SSH was not a success.
    if success == 0:
        svraddr = svrs[0]

#THIS COMMAND IS FOR LATER IN THE GAME
###Used to change the user's name. Not the one used when connected to servers,
###Just the one used on the local computer.
##def su(name1):
##    global place
##    global name
##    global username
##    #Check if the user is connected to a server. If they are, return an error.
##    if place != 1:
##        print('su can only be performed from your local computer')
##    #If they aren't connected to a server, but the length of the requested
##    #name is too small/big, return an error.
##    elif len(name1) < 1 or len(name1) > 15:
##        print("ERR: USER_NAME MUST BE BETWEEN 1 AND 15 CHARS~ ")
##    #If the criteria are met, change the name!
##    else:
##        print("[Process completed]\n")
##        name = name1
##        username = name1 + "$"

###Display various tips throughout the game
##def atip():
##    global level            #!!!!TO DO: MOVE THIS TO EMAIL: EMAIL EMPLOYER FROM LOCAL COMPUTER TO GET A TIP!!!!!
##    global tips
##    global tip
##    #Display the tip, depending on the level you are on.
##    for i in range(len(tip)):
##        #If your level is equal to the level of one of the tips in the list
##        if level == tip[i][1]:
##            #Print the tip
##            print(tip[i][0])
##            #Add one to the tips counter
##            tips += 1
##            #Exit the function
##            return
##    #If no tip was found for your level, print this
##    print("Sorry, no tip available for this level! You've got to figure it out on your own >:)")

#For exiting out of the current server, and returning to the user's computer.
def exit():
    global place
    global svr
    global svraddr
    global svrs
    global user
    #USE THIS WHEN CUSTOM NAMES ARE SUPPORTED
    #global name
    global username
    #Check the user is connected to a server
    if place == 1:
        print('Exit can only be performed from inside a server')
    #If the user is not connected to a server, set 'place' back to one and change
    #The user's name.
    else:
        #This is the only place the 'svr' variable is used :P
        print("""\nlogout
Connection to """ + svr + " closed.\n")
        place = 1
        svraddr = svrs[0]
        #USE THIS WHEN CUSTOM NAMES ARE SUPPORTED
        #user = name
        #username = name + '$'
        user = 'anonymous'
        username = 'anonymous$'
        #Update the email message tracker, in case of new emails
        emailcount = False

#This function is for simulating a command line based email client.
#Of course, this isn't how you would normally do email from bash.
def email():
    global user
    global emailaddr
    global addresses
    global level
    global emails
    global sent
    global send
    #Print a loading message
    print("Loading email client", end='')
    for i in range(3):
        time.sleep(1)
        print('.',end='')
    time.sleep(1)
    #Assign the user their email address, based upon their username.
    for i in range(len(addresses)):
        #If your username is the same as one of the entries in 'addresses'
        if user == addresses[i][0]:
            #Update the emailaddr variable.
            emailaddr = addresses[i][1]
    #Print an introductory message and the current email address
    print("\nClient loaded: " + emailaddr)
    print("type 'help' for a list of available commands.")
    #This client is supposedly like a seperated command line, it has its own commands.               When you think about it, this is a command line (email),
    #A clone of 'help' from the main command line                                                    inside of a command line (bash), inside of a command
    def ehelp():                                                                                     #line (python).... Trippy! o.O
        print("- help == display a list of available commands")                                      #(and maybe even another, depending on how you run the game)
        print("- inbox == display the inbox")
        print("- open <file number> == open an email. File number can be obtained with 'inbox'")
        print("- send <user>@<address> == send an email.")
        print("- sent == read your sent emails")
        print("- opensent <file> == read a sent email")
        print("- exit == close the email client")
    #A clone of 'ls' from the main command line, with a different database
    def einbox():
        print("\n=Inbox=")
        success = 0
        doccount = 0
        #Read from the emails array, for however many users are inside of it
        for i in range(len(emails)):
            #If the list of emails has the same address as yours
            if emails[i][0] == emailaddr:
                #Read through the emails list, for however many emails are listed
                for j in range(len(emails[i][1])):
                    #If you have the required level, print the email's name
                    if emails[i][1][j][2] <= level:
                        doccount += 1
                        print("(" + str(doccount) + ")", "-", emails[i][1][j][0], "from", emails[i][1][j][3], "on",emails[i][1][j][4])
                        success = 1
        if emailaddr == 'deeperresearch@gmail.com':
            for i in range(len(tip)):
                #Read through the tips list, for however many tips are listed
                #If you have the required level, print the tip's name
                if tip[i][2] <= level and tip[i][3] == True:
                    doccount += 1
                    print("(" + str(doccount) + ")", "-", tip[i][0], "from client456@gmail.com")
                    success = 1
        if success == 0:
            print("ERR: No files found")

    ###THE OLD EOPEN COMMAND###
##        #A clone of 'open' from the main command line, with a different database
##        def eopen(file):
##            doccount = 0
##            #Used to track whether or not the open was successful
##            success = 0
##            #Read from the emails array, for however many users are inside of it
##            for i in range(len(emails)):
##                #If the list of emails has the same address as yours
##                if emails[i][0] == emailaddr:
##                    #Read through the emails list, for however many emails are listed
##                    for j in range(len(emails[i][1])):
##                        #If you have the required level and the email has the same name as your request, print the email
##                        if emails[i][1][j][2] <= level and emails[i][1][j][0] == file:
##                            print(emails[i][1][j][1])
##                            success = 1
##            #If the open was not a success, print an error message
##            #This could have occured both because of incorrect file name in the request, or even if the user's level is too low.
##            if success == 0:
##                print("ERR: The email",file,"does not exist.")

    ###THE NEW EOPEN COMMAND####
    def eopen(file):
        doccount = 0
        success = 0
        #Read from the emails array, for however many users are inside of it
        for i in range(len(emails)):
            #If the list of emails has the same address as yours
            if emails[i][0] == emailaddr:
                #Read through the emails list, for however many emails are listed
                for j in range(len(emails[i][1])):
                    #If you have the required level
                    if emails[i][1][j][2] <= level:
                        doccount += 1
                        if doccount == file:
                            print("\n" + emails[i][1][j][1])
                            emails[i][1][j][5] = True
                            return
        if emailaddr == 'deeperresearch@gmail.com':
            for i in range(len(tip)):
                #Read through the tips list, for however many tips are listed
                #If you have the required level, print the tip's name
                if tip[i][2] <= level and tip[i][3] == True:
                    doccount += 1
                    if doccount == file:
                            print("\n" + tip[i][1])
                            tip[i][4] = True
                            return
        if success == 0:
            print("ERR: Invalid file number")

    #A clone of 'einbox,' with a different database
    def esent():
        print("\n=Sent Mail=")
        success = 0
        doccount = 0
        #Read from the emails array, for however many users are inside of it
        for i in range(len(sent)):
            #If the list of emails has the same address as yours
            if sent[i][0] == emailaddr:
                #Read through the emails list, for however many emails are listed
                for j in range(len(sent[i][1])):
                    #If you have the required level, print the email's name
                    if sent[i][1][j][2] <= level:
                        doccount += 1
                        print("(" + str(doccount) + ")", "-", sent[i][1][j][0], "to", sent[i][1][j][3], "on",emails[i][1][j][4])
                        success = 1
        if success == 0:
            print("ERR: No files found")

    #A clone of 'eopen,' with a different database
    def eopensent(file):
        doccount = 0
        success = 0
        #Read from the emails array, for however many users are inside of it
        for i in range(len(sent)):
            #If the list of emails has the same address as yours
            if sent[i][0] == emailaddr:
                #Read through the emails list, for however many emails are listed
                for j in range(len(sent[i][1])):
                    #If you have the required level
                    if sent[i][1][j][2] <= level:
                        doccount += 1
                        if doccount == file:
                            print("\n" + sent[i][1][j][1])
                            return
        if success == 0:
            print("ERR: Invalid file number")

    #This will later be used to send emails to npcs.
    def esend(sendto):
        doccount = 0
        success = 0
        for i in range(len(send)):
            if send[i][0] == emailaddr:
                for j in range(len(send[i][1])):
                    if send[i][1][j][2] <= level and send[i][1][j][3].lower() == sendto and checkrequire('esend',send[i][1][j][0],'') == True and send[i][1][j][4] == False:
                        print('(' + str(doccount) + ')','-',send[i][1][j][0])
                        doccount += 1
                        success = 1
        if success == 0:
            print("You have no reason to send any emails to this address right now.")
        else:
            opt = input('(' + str(doccount) + ') - cancel\n')
            while isnum(opt) == False:
                opt = input("ERR: Selection must be int\n")
            opt = int(opt)
            while opt < 0 or opt > doccount:
                opt = input("ERR: Selection must be between 0 and",doccount,'\n')
                while isnum(opt) == False:
                    opt = input("ERR: Selection must be int\n")
            opt = int(opt)
            doccount = 0
            for i in range(len(send)):
                if send[i][0] == emailaddr:
                    for j in range(len(send[i][1])):
                        if send[i][1][j][2] <= level and send[i][1][j][3].lower() == sendto and checkrequire('esend',send[i][1][j][0],'') == True:
                            if doccount == opt:
                                for k in range(len(send[i][1][j][1])):
                                    if not send[i][1][j][1][k] in ['.',':',';','\n']:
                                        time.sleep(0.045)
                                    else:
                                        time.sleep(1)
                                    print(send[i][1][j][1][k],end='')
                                option = input('\nsend? y/n: ').lower()
                                while not option in 'yn':
                                    option = input('send? y/n: ').lower()
                                if option == 'y':
                                    print('Sent.')
                                    send[i][1][j][4] = True
                                    for k in range(len(emails)):
                                        if emails[k][0] == send[i][1][j][3]:
                                            emails[k][1].append([send[i][1][j][0],send[i][1][j][1],send[i][1][j][2],emailaddr,'11/02/2015',False])
                                return
                            else:
                                doccount += 1



    #Notice exit doesnt have a function - partly because it's so simple, and partly
    #because I don't know how to exit a loop from a function.

    #Start the input loop
    while True:
    #take commands as input
        cmd = input('\nemail-client> ').lower().split(' ')
        #Test the given number of arguments by splitting the inputted string by the
        #space character, and then call the relative command
        if cmd[0] == 'help':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when help takes 0')
                printfact(3)
            else:
                ehelp()
        elif cmd[0] == 'inbox':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when inbox takes 0')
                printfact(3)
            else:
                einbox()
        elif cmd[0] == 'open':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when open takes 1')
                printfact(3)
            elif isnum(cmd[1]) == False:
                print("ERR: File number must be an integer")
            else:
                eopen(int(cmd[1]))
        elif cmd[0] == 'exit':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when exit takes 0')
                printfact(3)
            else:
                print("Email client closed.")
                return
        elif cmd[0] == 'sent':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when sent takes 0')
                printfact(3)
            else:
                esent()
        elif cmd[0] == 'send':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when send takes 1')
                printfact(3)
            else:
                if len(cmd[1].split('@')) != 2:
                    print('SYNTAX: send user@address')
                    printfact(4)
                else:
                    esend(cmd[1].lower())
        elif cmd[0] == 'opensent':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when opensent takes 1')
                printfact(3)
            elif isnum(cmd[1]) == False:
                print("ERR: File number must be an integer")
            else:
                eopensent(int(cmd[1]))
        else:
            print("-email: " + cmd[0] + ": command not found.")


#If the player get's stuck, this command will give them the solution
def cheat():
    global level
    global cheats
    if level < 2:
        print("Sorry, you can't cheat just yet! You're going to have to figure this one out on your own.\nDon't forget that you can email your client for a tip!")
    else:
        print("""Really? You want to cheat? Well... It's your choice I guess.
However, there has to be some fun in this, so i'm going to give you a maximum of 3
cheats.""")
        print("CHEATS LEFT:",cheats)
        if cheats == 0:
            print("Sorry, no more cheats left.. You're going to have to figure this out on your own.")
        else:
            x = input("Really cheat? type y or n: ")
            while x != 'y' and x != 'n':
                x = input("Choose y or n: ")
            if x == 'y':
                cheats -= 1
                if level == 2:
                    print("""==ANSWER AT THE BOTTOM==
I'm sorry, but If you're cheating at this stage, this may not be the game for you.
Firstly, we can run the command 'ls' to find out what files are on the current server. There's only one
file available to us on this server at the moment, and it's called location1.txt. So, let's run the
command 'cat location1.txt' to read it. The file says that we can access the first server in the
BioInnovations network with the IP address 97.73.9.646, and also that there is a new employee at
BioInnovations called Jeff, who hasen't yet changed his password from the default. So, let's run the
command 'ssh jeff@97.73.9.646' to access the server. You will now be prompted for Jeff's password, and
I don't doubt that's the bit you're stuck on. Now, there are quite a few default passwords which this
could have been, (e.g password, changeme, default, 0000 etc etc), and the answer (by guessing) is password.
===================================
Run the command 'ssh jeff@97.73.9.646 and enter password as the password when prompted.""")
                elif level == 3:
                    print("""==ANSWER AT THE BOTTOM==
I'm sorry, but If you're cheating at this stage, this may not be the game for you.
Firstly, let's launch Jeff's email client with the 'email' command. Upon using the email command
'inbox', we are shown an email called 10/02/2015, which is obviously also the date it was recieved.
The email can be opened by typing 'cat 10/02/2015'. When we read the email Jeff recieved on the 10th
of february, we discover some interesting information. Firstly, there is someone working in Senior
Management name J. Turner, he may be important later. We're also told that Jeff has an account on the main
company server with the same user name, Jeff. The password is supposedly the birth date of their most
recent client, one Mr. A. Johnstone. Let's close out of the email client with 'exit' and then see what
files Jeff has stored on his local drive with 'ls'. There's a file called 'recent_transactions.txt',
but unfortunately Jeff doesnt have the appropriate permissions to open this file. So, let's go into
the other file named 'client_profiles.txt' with 'cat client_profiles.txt'. Great! This file shows us
information on all of the clients BioInnovations exchanged goods and money with recently. The 1st
entry in the list is Andrew Johnstone, and the file tells us that his date of birth is 04/11/1958.
This will be the password.
Ok, so we have the user name and password, but we still don't know the address of the server... Let's go
back into the email client with 'email' and run 'inbox' again. There's another email from the 3rd of February,
so let's open that up with 'cat 11/02/2015'. Now we're getting somewhere, this email contains the server
address! It's 12.89.5.309. Easy peasy.
===================================
What a shame Jeff has broken his phone... Anyway, the answer to this level is to SSH into the server
12.89.5.309 with username Jeff and password 04/11/1958 In other words, run this command:
'ssh jeff@12.89.5.309', and then type 04/11/1958 once the password field appears.""")
            else:
                print("Good choice! Don't forget that you can email your client for a tip.")

#Used to download files to the local drive, when you don't have permission to open them in their original server
def scp(file):
    global place
    global user
    global level
    global scpcount
    #Used to track whether or not the file was found
    success = 0
    #Same basic idea as the ls() command.
    #Read from the docs array, for however many users are inside of it
    for i in range(len(docs)):
        #If the list of documents does not require a name or is the same as your name
        if docs[i][0] == "none" or docs[i][0] == user:
            #Read through the document list, for however many documents are listed
            for j in range(len(docs[i][1])):
                #If you have the required place and level, the file matches your search, and the file can be downloaded, download the document and set success to 1
                if docs[i][1][j][3] == place and docs[i][1][j][0] == file and docs[i][1][j][4] == True:
                    if docs[i][1][j][2] <= level:
                        doc = docs[i][1][j][1]
                        docname = docs[i][1][j][0]
                        docs[0][1].append([docname,doc,0,1,False, []])
                        print("FILE DOWNLOADED")
                        if scpcount == False:
                            print("\n\nP.S. The syntax for downloading files via ssh is slightly different\nto what I've used here, see this article: http://is.gd/9ERS8x")
                            scpcount = True
                    else:
                        print("ERR: ACCESS DENIED")
                    success = 1
    #If the open was not a success, an incorrect file name must have been requested. Print an error message
    if success == 0:
        print("ERR: The file",file,"does not exist.")
    elif success == 1:
        printfact(1)


#Introductory message to the game
print("""Welcome to the shell.
type 'help' for a list of available commands.""")

#Start main game loop
while True:
    getmail()
    #Check for emails if a message hasen't been shown already
    if emailcount == False:
        doccount = 0
        #Get user email address
        for i in range(len(addresses)):
            #If your username is the same as one of the entries in 'addresses'
            if user == addresses[i][0]:
                #Update the emailaddr variable.
                emailaddr = addresses[i][1]
                break

        #Read from the emails array, for however many users are inside of it
        for i in range(len(emails)):
            #If the list of emails has the same address as yours
            if emails[i][0] == emailaddr:
                #Read through the emails list, for however many emails are listed
                for j in range(len(emails[i][1])):
                    #If you have the required level and the email is unread, add to the document count
                    try:
                        emails[i][1][j][5]
                    except IndexError:
                        print(emails[i][1][j])
                    if emails[i][1][j][2] <= level and emails[i][1][j][5] == False:
                        doccount += 1

        #Also check the tips variable, but only if you have the right email.
        if emailaddr == 'deeperresearch@gmail.com':
            for i in range(len(tip)):
                #Read through the tips list, for however many tips are listed
                #If you have the required level and the email is unread, add to the document count
                if tip[i][2] <= level and tip[i][4] == False and tip[i][3] == True:
                    doccount += 1

        #Display message if there are any new emails.
        if doccount > 0:
            print("[!] You have",doccount,"new email(s)")
        emailcount = True

    #Take commands as input
    #Use a value from svrs to display the server name.
    cmd = input('\n' + svraddr[3] + ':~ ' + username + ' ').lower().split(' ')      #Some people get annoyed/confused with capitals, so I just set everything the user
                                                                                    #Inputs to lower case with the string.lower() command.
##    for i in range(len(cmds)): ##
##        if cmd == cmd[i][0]:   ##                     IN CASE YOU FIND A WAY TO CALL FUNCTIONS FROM AN ARRAY
##            cmd[i][0]          ##                     -> JUST BECAUSE THIS NEXT PROCESS IS SO INEFFICIENT
    #Test the given number of arguments by splitting the inputted string by the
    #space character, and then call the relative command
    if cmd != ['']:
        print()
        if cmd[0] == 'help':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when help takes 0')
                printfact(3)
            else:
                help()
        elif cmd[0] == 'ls':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when ls takes 0')
                printfact(3)
            else:
                ls()
        elif cmd[0] == 'cat':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when open takes 1')
                printfact(3)
            else:
                cat(str(cmd[1]))
        elif cmd[0] == 'ssh':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when ssh takes 1')
                printfact(3)
            else:
                if len(cmd[1].split('@')) != 2:
                    print('SYNTAX: ssh user@address')
                    printfact(4)
                else:
                    ssh(cmd[1].split('@')[0],cmd[1].split('@')[1])
                    emailcount = False
        #THIS COMMAND IS FOR LATER IN THE GAME
##        elif cmd[0] == 'su':
##            if len(cmd) != 2:
##                print(str(len(cmd)-1) + ' arguments given when su takes 1')
##                printfact(3)
##            else:
##                su(cmd[1])
        elif cmd[0] == 'exit':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when exit takes 0')
                printfact(3)
            else:
                exit()
                emailcount = False
        #elif cmd[0] == 'atip':
        #    if len(cmd) != 1:
        #        print(str(len(cmd)-1) + ' arguments given when atip takes 0')
        #        printfact(3)
        #    else:
        #        atip()
        elif cmd[0] == 'email':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when email takes 0')
                printfact(3)
            else:
                email()
                emailcount = False
        elif cmd[0] == 'cheat':
            if len(cmd) != 1:
                print(str(len(cmd)-1) + ' arguments given when cheat takes 0')
                printfact(3)
            else:
                cheat()
                emailcount = False
        elif cmd[0] == 'scp':
            if len(cmd) != 2:
                print(str(len(cmd)-1) + ' arguments given when scp takes 1')
                printfact(3)
            else:
                scp(cmd[1])
        #If the command inputted was not within the list of valid commands,
        #Give an error.
        else:
            #Depending on where the user is (server-wise), give the relative protocol.
            if place == 1:
                method = 'bash'
            else:
                method = 'sh'
            print('-' + method + ': ' + cmd[0] + ': command not found')
