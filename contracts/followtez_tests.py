import smartpy as sp


FollowTez = sp.io.import_script_from_url("https://raw.githubusercontent.com/spangin/followtez/main/contracts/followtez.py").FollowTez


##############################################################################

# Tests
@sp.add_test(name = "FollowTez")
def test():
    userA = sp.test_account("UserA")
    userB = sp.test_account("UserB")
    userC = sp.test_account("UserC")
    scenario = sp.test_scenario()
    scenario.h1("FollowTez tests")
    followtez = FollowTez()
    scenario += followtez

    followtez.follow(userA.address).run(sender = userC)
    followtez.follow(userA.address).run(sender = userC, valid = False)
    followtez.follow(userA.address).run(sender = userB)
    followtez.follow(userB.address).run(sender = userC)
    followtez.unfollow(userB.address).run(sender = userC)
    followtez.unfollow(userA.address).run(sender = userC)
    followtez.unfollow(userC.address).run(sender = userA, valid = False)

