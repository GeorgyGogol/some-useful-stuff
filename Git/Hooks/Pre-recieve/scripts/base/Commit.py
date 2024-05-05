import re

class BranchException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class CommitInfo:
    __BranchRegex = 'refs\/heads\/(.*)'

    def __init__(self, rawInfo: list) -> None:                
        self.Branch = CommitInfo.__defineBranchName(rawInfo[1])
        self.Hash = str(rawInfo[2])
        self.Author = str(rawInfo[3])
        self.Message = str(rawInfo[4])
        pass

    def __defineBranchName(rawName : str) -> str:
        regexResult = re.search(CommitInfo.__BranchRegex, rawName)
        if not regexResult:
            raise BranchException("Error: There are not branch")
        return regexResult.group(1)

    def __str__(self) -> str:
        out : str = ''
        out += 'Commit info:\n'
        out += 'Branch: ' + self.Branch  + '\n'
        out += 'Hash: ' + self.Hash + '\n'
        out += 'Author: ' + self.Author + '\n'
        out += 'Message: ' + self.Message
        return out

