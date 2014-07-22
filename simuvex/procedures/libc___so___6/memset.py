import simuvex

import logging
l = logging.getLogger("simuvex.procedures.libc.memset")

######################################
# memset
######################################

class memset(simuvex.SimProcedure):
	def __init__(self): # pylint: disable=W0231
		dst_addr = self.arg(0)
		char = self.arg(1)[7:0]
		num = self.arg(2)

		if self.state.symbolic(num):
			l.debug("symbolic length")
			max_size = self.state.min_int(num) + self.state['libc'].max_buffer_size
			write_bytes = self.state.claripy.Concat(*([ char ] * max_size))
			self.state.store_mem(dst_addr, write_bytes, symbolic_length=num)
		else:
			max_size = self.state.any_int(num)
			write_bytes = self.state.claripy.Concat(*([ char ] * max_size))
			self.state.store_mem(dst_addr, write_bytes)

			l.debug("memset writing %d bytes", max_size)

		self.add_refs(simuvex.SimMemWrite(self.addr, self.stmt_from, dst_addr, write_bytes, max_size*8, [], [], [], []))
		self.ret(dst_addr)
