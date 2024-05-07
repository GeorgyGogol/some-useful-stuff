import os
#import MessageRules
#import LineRule

import re

class LineRule:
    def __init__(self) -> None:
        self.__MaxLength = None
        self.__Regex = None

    def __str__(self) -> str:
        out = str()
        out += 'Rule:'
        if self.__MaxLength:
            out += '\nMaxLength: ' + self.__MaxLength
        if self.__Regex:
            out += '\nRegex: ' + self.__Regex
        return out

    def setMaxLength(self, length : int) -> None:
        self.__MaxLength = length
        self.__Regex = None

    def setRegex(self, regex : str) -> None:
        self.__MaxLength = None
        self.__Regex = regex[:-1]

    @property
    def MaxLength(self) -> int:
        return self.__MaxLength

    @MaxLength.setter
    def MaxLength(self, value : int):
        self.setMaxLength(value)

    @property
    def Regex(self) -> str:
        return self.__Regex

    @Regex.setter
    def Regex(self, value : str):
        self.setRegex(value)

    def Valid(self, string : str) -> bool:
        isOkay = False
        if self.__Regex:
            isOkay = bool(re.search(self.__Regex, string))
        elif self.__MaxLength:
            isOkay = len(string) < self.__MaxLength
        return isOkay


class MessageRules:
    def __init__(self) -> None:
        self.Header = LineRule()
        self.Header.MaxLength = 50
        self.Body = LineRule()
        self.Body.MaxLength = 72


class BranchRules:
    def __init__(self, branchName : str) -> None:
        self.__Name = branchName
        self.__isProtected = False
        self.__AllowedUsers = list()
        self.__MessageRules = MessageRules()
        self.__LoadBranchRules()

    def __LoadBranchRules(self) -> None:
        securityDir = os.getcwd() + '\\hooks\\security\\'

        try:
            allowedUsers = open(securityDir + 'AllowedUsers\\' + self.BranchName, 'r')
            #if allowedUsers:
            self.__isProtected = True
            self.__AllowedUsers = allowedUsers.readlines()
            allowedUsers.close()
        except:
            pass

        commitStyles = None
        try:
            commitStyles = open(securityDir + 'commitStyles\\' + self.BranchName, 'r')
        except:
            try:
                commitStyles = open(securityDir + 'commitStyles\\default.style', 'r')
            except:
                commitStyles = None

        if not commitStyles:
            return

        headerLine = str(commitStyles.readline())
        # bodyLine = str(commitStyles.readlines())

        self.__MessageRules.Header = BranchRules.__ReadLineRule(headerLine)
        self.__MessageRules.Body.MaxLength = 72

        commitStyles.close()

    def __ReadLineRule(line : str) -> LineRule:
        rule = LineRule()
        if line.find("len:") == 0:
            rule.MaxLength = int(line[4:])
        else:
            rule.Regex = line
        return rule

    @property
    def IsBranchProtected(self) -> bool:
        return self.__isProtected

    @property
    def BranchName(self) -> str:
        return self.__Name

    def IsHaveAccess(self, user : str) -> bool:
        return user in self.__AllowedUsers

    def VerifyMessage(self, message : str) -> bool:
        newLinePos = message.find('\n')
        headerMessage = str()
        bodyMessage = str()

        if newLinePos > 0:
            headerMessage = message[:newLinePos]
            bodyMessage = message[newLinePos + 2:]
        else:
            headerMessage = message

        if not headerMessage:
            return False

        isHeaderValid = self.__MessageRules.Header.Valid(headerMessage)

        isBodyValid = True
        if bodyMessage:
            isBodyValid = self.__MessageRules.Body.Valid(bodyMessage)

        return isHeaderValid and isBodyValid


