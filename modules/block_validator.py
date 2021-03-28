from modules.chain_validation import hash, is_chain_valid
import copy



def is_block_valid(block, chain):
	chain_temp = copy.deepcopy(chain)
	#Validating transactions in the new block
	block_valid = True

	#Validating the chain with new block
	if block_valid:
		chain_temp.append(block)
		chain_valid = is_chain_valid(chain_temp)

		if chain_valid and block_valid:
			return True
		else:
			return False

	else:
		return False
