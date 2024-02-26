import smartpy as sp


class FollowTez(sp.Contract):

    def __init__(self):
        self.init(
            followers = sp.big_map(tkey = sp.TRecord(f = sp.TAddress, l = sp.TAddress), tvalue = sp.TUnit),
            stats = sp.big_map(tkey = sp.TAddress, tvalue = sp.TRecord(f = sp.TNat, l = sp.TNat))
        )

    
    @sp.onchain_view()
    def get_stats(self, address):
        sp.result(self.data.stats.get_opt(address))

    
    @sp.onchain_view()
    def check(self, params):
        sp.set_type(params, sp.TRecord(f = sp.TAddress, l = sp.TAddress))
        sp.result(self.data.followers.contains(params))


    @sp.entry_point()
    def follow(self, address):
        sp.set_type(address, sp.TAddress)
        k = sp.local("k", sp.record(f = sp.sender, l = address))
        sp.verify(~self.data.followers.contains(k.value), message = "FOLLOWTEZ_ERR already done")
        self.data.followers[k.value] = sp.unit
        sf = sp.local("sf", self.data.stats.get(sp.sender, default_value = sp.record(l = sp.nat(0), f = sp.nat(0))))
        sf.value.l += 1
        self.data.stats[sp.sender] = sf.value
        sl = sp.local("sl", self.data.stats.get(address, default_value = sp.record(l = sp.nat(0), f = sp.nat(0))))
        sl.value.f += 1
        self.data.stats[address] = sl.value

    
    @sp.entry_point()
    def unfollow(self, address):
        sp.set_type(address, sp.TAddress)
        k = sp.local("k", sp.record(f = sp.sender, l = address))
        sp.verify(self.data.followers.contains(k.value), message = "FOLLOWTEZ_ERR not found")
        del self.data.followers[k.value]
        sf = sp.local("sf", self.data.stats.get(sp.sender, message = "FOLLOWTEZ_ERR no stats"))
        sf.value.l = sp.as_nat(sf.value.l - 1)
        self.data.stats[sp.sender] = sf.value
        sl = sp.local("sl", self.data.stats.get(address, message = "FOLLOWTEZ_ERR no stats"))
        sl.value.f = sp.as_nat(sl.value.f - 1)
        self.data.stats[address] = sl.value
