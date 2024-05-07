import sys
import base.Commit
import base.BranchRules

# Define commit info and load rules
commit = base.Commit.CommitInfo(sys.argv)
rules = base.BranchRules.BranchRules(commit.Branch)

# Check branch rules
if rules.IsBranchProtected:
    print("Warning: You push to protected branch")
    if not rules.IsHaveAccess(commit.Author):
        print("Error: You don't have access to push in this branch")
        sys.exit(1)

# Check commit message
if not rules.VerifyMessage(commit.Message):
    print("Error: Commit message is not valid")
    sys.exit(2)

