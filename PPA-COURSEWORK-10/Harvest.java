public class Harvest {

	public static void main(String[] args) {
		Farm farm = new Farm();

		farm.addHarvester(new Harvester(1, 1));
		farm.addHarvester(new CombineHarvester(2, 2, 3));

		for (int i = 0; i < 5; i++) {
			farm.addField("corn", 20);
			farm.addField("wheat", 20);
			farm.addField("oats", 20);
			farm.addField("barley", 20);
		}

		farm.harvest();

		System.out.println(farm.getProfit());
	}
}
