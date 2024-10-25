from typing import TypeAlias





# Datasets
_DatasetItem: TypeAlias = dict[str, str]
_DatasetsItemList: TypeAlias = list[_DatasetItem]
_DatasetsSection: TypeAlias = dict[str, _DatasetsItemList]

# Docs
_DocsItem: TypeAlias = dict[str, str]
_DocsItemList: TypeAlias = list[_DocsItem]
_DocsSection: TypeAlias = dict[str, _DocsItemList]

# Model 
_ModelPartItem: TypeAlias = dict[str, str]
_ModelPartItemList: TypeAlias = list[_ModelPartItem]
_ModelContents: TypeAlias = dict[str, str | _ModelPartItemList]
_ModelSection: TypeAlias = dict[str, _ModelContents]




