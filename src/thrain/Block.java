package thrain;
import java.util.Arrays;

/*This class is representation of what information shall each block have. The block also generates
 * hash signature based on signature of previous block and the data present in the current block.
 */

public class Block {

	//Previous Hash is the signature of the previous block used to maintain the list
	private int previousHash;
	//Transaction is the list of transactions we make
	private String[] transactions;
	
	//Hash Previous Hash and transactions to get a new signature of the current block
	//NOTE: The signature changes if any of the parameter of the hashCode function changes
	private int currentBlockHash;
	
	Block(int previousHash, String [] transactions){
		
		this.previousHash = previousHash;
		this.transactions = transactions;
		
		Object [] value = {Arrays.hashCode(transactions),previousHash};
		this.currentBlockHash = Arrays.hashCode(value);
	}
	
	public int getPreviousHash() {
		
		return previousHash;
	}
	
	public String[] getTransaction() {
		return transactions;
	}
}
