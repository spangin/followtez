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

    followtez.follow(address = userA.address, is_source = False).run(sender = userC)
    scenario.verify(followtez.check(sp.record(l = userA.address, f = userC.address)))
    followtez.follow(address = userA.address, is_source = False).run(sender = userC, valid = False)
    followtez.follow(address = userA.address, is_source = False).run(sender = userB)
    followtez.follow(address = userB.address, is_source = False).run(sender = userC)
    followtez.unfollow(address = userB.address, is_source = False).run(sender = userC)
    followtez.unfollow(address = userA.address, is_source = False).run(sender = userC)
    followtez.unfollow(address = userC.address, is_source = False).run(sender = userA, valid = False)
