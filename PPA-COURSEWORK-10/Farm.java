import java.util.ArrayList;

public class Farm {

	private ArrayList<Field> fields;
	private ArrayList<Harvester> harvesters;
	private int profit;

	public Farm() {
		fields = new ArrayList<Field>();
		harvesters = new ArrayList<Harvester>();
	}

	public int getProfit() {
		return profit;
	}

	public void addHarvester(Harvester harvester) {
		this.harvesters.add(harvester);
	}

	public void addField(String type, int value) {
		fields.add(new Field(type, value));
	}

	public void harvest() {
		int totalHarvestingCapacity = 0;
		for (Harvester harvester : harvesters) {
			totalHarvestingCapacity += harvester.getHarvestingCapacity();
		}

		for (int i = 0; i < totalHarvestingCapacity; i++) {
			profit += fields.get(i).harvest();
		}
	}
}
