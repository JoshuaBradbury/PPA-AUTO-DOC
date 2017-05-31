public class CombineHarvester extends Harvester {

	private int length;

	public CombineHarvester(int fuelTankSize, int topSpeed, int length) {
		super(fuelTankSize, topSpeed);
		setHarvestingCapacity(getHarvestingCapacity() * length);
	}
}
