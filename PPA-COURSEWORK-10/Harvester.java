public class Harvester {

	private int fuelTankSize, topSpeed, harvestingCapacity;

	public Harvester(int fuelTankSize, int topSpeed) {
		this.fuelTankSize = fuelTankSize;
		this.topSpeed = topSpeed;
		harvestingCapacity = fuelTankSize + topSpeed;
	}

	public int getHarvestingCapacity() {
		return harvestingCapacity;
	}

	public void setHarvestingCapacity(int harvestingCapacity) {
		this.harvestingCapacity = harvestingCapacity;
	}
}
