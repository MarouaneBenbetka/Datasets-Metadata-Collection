import json


def join_json_files(json_files, output_file):
    """
    Join multiple JSON files into a single file.

    Args:
    json_files (List[str]): List of file paths to JSON files.
    output_file (str): File path to write the joined JSON data to.

    Returns:
    None
    """
    joined_data = []
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf8') as f:
                data = json.load(f)
                joined_data.extend(data)
        except Exception as e:
            print(e)

    with open(output_file, 'w', encoding='utf8') as file:
        json.dump(joined_data, file)


json_files = [
    f"./datasets/hugging-face/hugging-face-{i}.json" for i in range(5, 236, 5)]

join_json_files(json_files, "./datasets/hugging-face/hugging-face.json")
