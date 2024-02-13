from datetime import datetime
import json
current_datetime = datetime.utcnow()
formatted_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

source = {
    "name": "Hugging Face",
    "url": "https://huggingface.co/datasets",
    "description": "Hugging Face is a platform that provides a comprehensive collection of natural language processing (NLP) models, tools, and resources for developers and researchers."
}


licenses_dict = {
    "odc-by": {
        "name": "ODC Attribution License (ODC-By)",
        "url": "https://opendatacommons.org/licenses/by/",
        "description": "ODC Attribution License allows users to freely share, modify, and use data as long as they provide attribution to the original source."
    },
    "mit": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
        "description": "The MIT License is a permissive open source license recognized for its simplicity and flexibility. It allows users to do anything they want with the code as long as they provide attribution and include the original license in any copy or substantial portion of the software."
    },
    "cc-by-nd-4.0": {
        "name": "Creative Commons Attribution-NoDerivatives 4.0 International License (CC-BY-ND-4.0)",
        "url": "https://creativecommons.org/licenses/by-nd/4.0/",
        "description": "This license allows others to download the works and share them with others as long as they credit the author, but they can’t change them in any way or use them commercially."
    },
    "cc0-1.0": {
        "name": "Creative Commons Zero v1.0 Universal (CC0-1.0)",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "description": "CC0 enables scientists, educators, artists, and other creators and owners of copyright- or database-protected content to waive those interests in their works and thereby place them as completely as possible in the public domain, so that others may freely build upon, enhance, and reuse the works for any purposes without restriction under copyright or database law."
    },
    "cc-by-2.5": {
        "name": "Creative Commons Attribution 2.5 Generic License (CC-BY-2.5)",
        "url": "https://creativecommons.org/licenses/by/2.5/",
        "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you for the original creation. This is the most flexible of the licenses offered, in terms of what others can do with your works."
    },
    "apache-2.0": {
        "name": "Apache License 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
        "description": "The Apache License is a permissive free software license written by the Apache Software Foundation. It allows users to use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software under the terms of the license."
    },
    "cc-by-nc-sa-3.0": {
        "name": "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License (CC-BY-NC-SA-3.0)",
        "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/",
        "description": "This license lets others remix, tweak, and build upon your work non-commercially, as long as they credit you and license their new creations under the identical terms."
    },
    "bsd-3-clause": {
        "name": "BSD 3-Clause License",
        "url": "https://opensource.org/licenses/BSD-3-Clause",
        "description": "The BSD 3-Clause License is a permissive free software license written by the University of California. It allows users to use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software under the terms of the license."
    },
    "cc-by-3.0": {
        "name": "Creative Commons Attribution 3.0 Unported License (CC-BY-3.0)",
        "url": "https://creativecommons.org/licenses/by/3.0/",
        "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you and license their new creations under the identical terms. This license is often compared to open source software licenses."
    },
    "cc-by-sa-3.0": {
        "name": "Creative Commons Attribution-ShareAlike 3.0 Unported License (CC-BY-SA-3.0)",
        "url": "https://creativecommons.org/licenses/by-sa/3.0/",
        "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you and license their new creations under the identical terms."
    },
    "cc-by-nc-sa-4.0": {
        "name": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC-BY-NC-SA-4.0)",
        "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "description": "This license lets others remix, tweak, and build upon your work non-commercially, as long as they credit you and license their new creations under the identical terms."
    },
    "cc-by-sa-4.0": {
        "name": "Creative Commons Attribution-ShareAlike 4.0 International License (CC-BY-SA-4.0)",
        "url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you and license their new creations under the identical terms."
    },
    "gpl-3.0": {
        "name": "GNU General Public License v3.0 (GPL-3.0)",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
        "description": "The GNU General Public License is a widely used free software license that guarantees end users the freedom to run, study, share, and modify the software."
    },
    "gfdl": {
        "name": "GNU Free Documentation License (GFDL)",
        "url": "https://www.gnu.org/licenses/fdl-1.3.html",
        "description": "The GNU Free Documentation License is a copyleft license for free documentation, designed by the Free Software Foundation for the GNU Project."
    },
    "cc-by-4.0": {
        "name": "Creative Commons Attribution 4.0 International License (CC-BY-4.0)",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "description": "This license lets others remix, tweak, and build upon your work, even commercially, as long as they credit you for the original creation. This is the most flexible of the licenses offered, in terms of what others can do with your works."
    },
    "agpl-3.0": {
        "name": "GNU Affero General Public License v3.0 (AGPL-3.0)",
        "url": "https://www.gnu.org/licenses/agpl-3.0.html",
        "description": "The GNU Affero General Public License is a free, copyleft license for software and other kinds of works, specifically designed to ensure cooperation with the community in the case of network server software."
    },
    "cc-by-nc-4.0": {
        "name": "Creative Commons Attribution-NonCommercial 4.0 International License (CC-BY-NC-4.0)",
        "url": "https://creativecommons.org/licenses/by-nc/4.0/",
        "description": "This license lets others remix, tweak, and build upon your work non-commercially, as long as they credit you and license their new creations under the identical terms."
    },
    "c-uda": {
        "name": "CUDA EULA",
        "url": "https://developer.nvidia.com/cuda-eula",
        "description": "The CUDA End User License Agreement (EULA) is the license agreement for NVIDIA's CUDA toolkit, a parallel computing platform and application programming interface model."
    }
}


unknown_license = {
    "name": "unknown",
    "url": "",
    "description": "The license is unknown, and details about its terms and conditions are not specified."
},


base_url = "https://huggingface.co/datasets"

licenses_unique = set()


def clean_dataset(dataset):

    clean_dataset = {}
    clean_dataset["title"] = dataset.get("id", "")
    clean_dataset["url"] = base_url+dataset.get("id", "")
    arxiv_id = dataset.get('infos', {}).get("arxiv", "")
    if arxiv_id:
        arxiv_redirect_text = f"\n You can find more information about this dataset on Arxiv: https://arxiv.org/abs/{arxiv_id}"
    else:
        arxiv_redirect_text = ""
    clean_dataset["description"] = dataset.get(
        "description", f"{clean_dataset['title']} \n {dataset.get('subtitle','')} {arxiv_redirect_text}")
    clean_dataset["totalBytes"] = int(dataset.get("dataset_size", 0))
    clean_dataset["createdAt"] = dataset.get("lastUpdated", formatted_date)
    clean_dataset["source"] = source
    clean_dataset["stats"] = {
        "viewCount": None,
        "likes_count": int(dataset.get("likes", 0)),
        "downloadCount": int(dataset.get("download", 0)),
    }

    author = dataset.get("author", None)
    if author:
        clean_dataset["owners"] = [
            {
                "name": author,
                "ref": "https://huggingface.co/" + dataset.get("owner", {}).get("ref", "")
            }
        ]
    else:
        clean_dataset["owners"] = []

    tags = []
    for key, value in dataset.get("infos", {}).items():
        if key in ["license", "language"] or value.lower() in ["other", "unknown", "", "none", None]:
            continue
        tags += [value.lower()]

    clean_dataset["tags"] = tags

    license = dataset.get("infos", {}).get("license", None)
    if license:
        licenses_unique.add(license)
        # clean_dataset["license"] = licenses_dict.get(
        #     license, unknown_license
        # )
    else:
        clean_dataset["license"] = None

    clean_dataset["notebooks"] = []
    clean_dataset["descussions"] = []

    features = []
    for feature, type in dataset.get("features", {}).items():
        features += [{
            "name": feature,
            "type": type,
            "description": ""
        }]
    clean_dataset["features"] = features
    use_case = dataset.get("infos", {}).get("task_categories", None)
    if use_case:
        clean_dataset["useCases"] = [use_case]
    else:
        clean_dataset["useCases"] = []

    clean_dataset["issues"] = []

    return clean_dataset


result = []
with open('./datasets/hugging-face/hugging-face.json', 'r') as file:
    data = json.load(file)
    for dataset in data:
        try:
            result += [clean_dataset(dataset)]
        except Exception as e:
            print(f"Error in this dataset: {dataset.get('ref', 'unknown')}")
            print(e)


print(f"Unique licenses: {list(licenses_unique)}")
with open('./datasets/hugging-face/hugging-face-cleaned.json', 'w') as file:
    json.dump(result, file)
