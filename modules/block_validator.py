from modules.chain_validation import hash, is_chain_valid
import copy

# Function that verifies if a given block is valid (incomplete)
def is_block_valid(block, chain):
	chain_temp = copy.deepcopy(chain)
	#Validating transactions in the new block, for now we assume it's true
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
