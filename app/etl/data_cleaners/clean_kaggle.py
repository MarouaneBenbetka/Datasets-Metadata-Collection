from datetime import datetime
import json
current_datetime = datetime.utcnow()
formatted_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

source = {
    "name": "Kaggle",
    "url": "https://www.kaggle.com/datasets",
    "description": "Kaggle is the world's largest data science community with powerful tools and resources to help you achieve your data science goals."
}


licenses_dict = {
    "ODC Attribution License (ODC-By)": {
        "name": "ODC Attribution License (ODC-By)",
        "url": "https://opendatacommons.org/licenses/by/",
        "description": "ODC Attribution License allows users to freely share, modify, and use data as long as they provide attribution to the original source."
    },
    "DbCL-1.0": {
        "name": "DbCL-1.0",
        "url": "https://opendatacommons.org/licenses/dbcl/1.0/",
        "description": "DbCL-1.0 is the Database Contents License, version 1.0, providing terms for using and sharing database contents."
    },
    "Attribution 4.0 International (CC BY 4.0)": {
        "name": "Attribution 4.0 International (CC BY 4.0)",
        "url": "https://creativecommons.org/licenses/by/4.0/",
        "description": "CC BY 4.0 allows users to copy, distribute, display, and perform the work and derivative works based upon it but only if they give the author or licensor the credits in the manner specified by these."
    },
    "Apache 2.0": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
        "description": "The Apache License 2.0 is a permissive free software license written by the Apache Software Foundation, allowing users to use the software for any purpose, to distribute it, to modify it, and to distribute modified versions of the software under the terms of the license."
    },
    "CC-BY-NC-SA-4.0": {
        "name": "CC-BY-NC-SA-4.0",
        "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        "description": "CC BY-NC-SA 4.0 allows users to copy, distribute, display, and perform the work and derivative works based upon it but only for non-commercial purposes, giving appropriate credit, and under the same license terms."
    },
    "CC0-1.0": {
        "name": "CC0-1.0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "description": "CC0-1.0 is a public domain dedication, waiving all copyright and related rights. Users can copy, modify, distribute, and perform the work, even for commercial purposes, without asking for permission."
    },
    "MIT": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
        "description": "The MIT License is a permissive free software license originating at the Massachusetts Institute of Technology, allowing users to use, modify, and distribute the software for any purpose."
    }
}


unknown_license = {
    "name": "unknown",
            "url": "",
            "description": "The license is unknown, and details about its terms and conditions are not specified."
},


base_url = "https://www.kaggle.com/datasets/"


def clean_kaggle_dataset(dataset):

    clean_dataset = {}

    clean_dataset["title"] = dataset.get("title", "")
    clean_dataset["url"] = base_url+dataset.get("ref", "")
    clean_dataset["description"] = dataset.get(
        "description", f"{clean_dataset['title']} \n {dataset.get('subtitle','')}")
    clean_dataset["totalBytes"] = int(dataset.get("totalBytes", 0))
    clean_dataset["creation_date"] = dataset.get("lastUpdated", formatted_date)
    clean_dataset["source"] = source
    clean_dataset["stats"] = {
        "viewCount": int(dataset.get("stats", {}).get("viewCount", 0)),
        "likes_count": int(dataset.get("stats", {}).get("voteCount", 0)),
        "downloadCount": int(dataset.get("stats", {}).get("downloadCount", 0)),
    }
    clean_dataset["owners"] = [
        {
            "name": dataset.get("owner", {}).get("name", ""),
            "ref": dataset.get("owner", {}).get("ref", "")
        }
    ]

    clean_dataset["tags"] = dataset.get("keywords", [])
    licenses = dataset.get("licenses", None)
    if licenses and licenses[0]:
        clean_dataset["license"] = licenses_dict.get(
            licenses[0].get("name", ""), unknown_license
        )
    else:
        clean_dataset["license"] = None

    clean_dataset["notebooks"] = dataset.get("notebooks", [])
    clean_dataset["descussions"] = dataset.get("descussion", [])

    clean_dataset["features"] = []
    clean_dataset["useCases"] = []
    clean_dataset["issues"] = []

    return clean_dataset


# result = []
# with open('./datasets/kaggle/kaggle.json', 'r') as file:
#     data = json.load(file)
#     for dataset in data:
#         try:
#             result += [clean_dataset(dataset)]
#         except Exception as e:
#             print(f"Error in this dataset: {dataset.get('ref', 'unknown')}")
#             print(e)


# with open('./datasets/kaggle/kaggle-cleaned.json', 'w') as file:
#     json.dump(result, file)
