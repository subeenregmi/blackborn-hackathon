import smartpy as sp

sender = sp.TAddress
amount = sp.TMutez
tx = sp.TMap(sender, amount)

class escrowSystem(sp.Contract):
    def __init__(self):
        self.init_type(tx)
        self.init({})   

    @sp.entry_point()
    def deposit(self):
        sp.if ~(self.data.contains(sp.sender)):
            self.data = sp.update_map(self.data, sp.sender, sp.some(sp.amount))
        sp.else:
            self.data[sp.sender] += sp.amount

        
    @sp.entry_point()
    def withdraw(self, params):
        sp.set_type(params, sp.TMutez)
        sp.verify(self.data[sp.sender] >= params)
        self.data[sp.sender] -= params
        sp.send(sp.sender, params, message="sent")


@sp.add_test(name = "escrowSystem")
def test():
    scenario = sp.test_scenario()
    contract = escrowSystem()
    scenario += contract
    subeen = sp.test_account("Subeen")
    hamzah = sp.test_account("Hamaza")

    contract.deposit().run(sender = subeen, amount = sp.mutez(10))
    contract.deposit().run(sender = hamzah, amount = sp.mutez(20))
    contract.withdraw(sp.mutez(5)).run(sender = subeen)
    contract.deposit().run(sender = subeen, amount = sp.mutez(0))
    contract.withdraw(sp.mutez(20)).run(sender = hamzah)
    contract.deposit().run(sender = subeen, amount = sp.mutez(0))

