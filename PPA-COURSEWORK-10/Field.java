import java.util.ArrayList;

public class Field {

	public ArrayList<Crop> crops;
	private String type;
	private int value;

	public Field(String type, int value) {
		crops = new ArrayList<Crop>();
		this.type = type;
		this.value = value;
		plant();
	}

	public void plant() {
		for (int i = crops.size(); i < 10; i++) {
			crops.add(new Crop(type, value));
		}
	}

	public int harvest() {
		int totalValue = 0;

		for (Crop crop : crops) {
			totalValue += crop.getValue();
		}
		crops.clear();

		return totalValue;
	}
}
