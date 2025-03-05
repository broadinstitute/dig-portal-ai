# Auto generated from portal-model.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-28T19:00:38
# Schema: a2f-portal
#
# id: https://w3id.org/a2f/portal-model
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DATACOMMONS = CurieNamespace('DATACOMMONS', 'https://datacommons.org/browser/')
EFO = CurieNamespace('EFO', 'http://identifiers.org/efo/')
ENSEMBL = CurieNamespace('ENSEMBL', 'http://identifiers.org/ensembl/')
GCST = CurieNamespace('GCST', 'http://identifiers.org/gcst/')
HGNC = CurieNamespace('HGNC', 'http://identifiers.org/hgnc/')
HGNC_SYMBOL = CurieNamespace('HGNC_SYMBOL', 'http://identifiers.org/hgnc.symbol/')
MGI = CurieNamespace('MGI', 'http://identifiers.org/MGI/')
NCBIGENE = CurieNamespace('NCBIGene', 'http://identifiers.org/ncbigene/')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
PORTAL_DATASET = CurieNamespace('PORTAL_DATASET', 'https://a2f.hugeamp.org/dinspector.html?dataset=')
PORTAL_GENESET = CurieNamespace('PORTAL_GENESET', 'http://example.org/UNKNOWN/PORTAL.GENESET/')
SIO = CurieNamespace('SIO', 'http://identifiers.org/sio/')
SO = CurieNamespace('SO', 'http://purl.obolibrary.org/obo/SO_')
WIKIDATA = CurieNamespace('WIKIDATA', 'http://identifiers.org/wikidata/')
ZFIN = CurieNamespace('ZFIN', 'http://identifiers.org/zfin/')
A2F = CurieNamespace('a2f', 'https://w3id.org/a2f/')
DCID = CurieNamespace('dcid', 'http://example.org/UNKNOWN/dcid/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = CurieNamespace('', 'https://w3id.org/a2f/portal-model/')


# Types

# Class references
class GeneId(extended_str):
    pass


class PhenotypeId(extended_str):
    pass


class AssociationId(extended_str):
    pass


class DirectSupportAssociationId(AssociationId):
    pass


class IndirectSupportAssociationId(extended_str):
    pass


class CombinedSupportAssociationId(extended_str):
    pass


class GwasId(extended_str):
    pass


class GeneSetId(extended_str):
    pass


class GeneSetJointEffectAssociationId(AssociationId):
    pass


class GeneSetMarginalEffectAssociationId(AssociationId):
    pass


@dataclass(repr=False)
class Gene(YAMLRoot):
    """
    A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A
    gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/Gene"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/Gene"
    class_name: ClassVar[str] = "Gene"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/Gene")

    id: Union[str, GeneId] = None
    symbol: Optional[str] = None
    has_xrefs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneId):
            self.id = GeneId(self.id)

        if self.symbol is not None and not isinstance(self.symbol, str):
            self.symbol = str(self.symbol)

        if not isinstance(self.has_xrefs, list):
            self.has_xrefs = [self.has_xrefs] if self.has_xrefs is not None else []
        self.has_xrefs = [v if isinstance(v, str) else str(v) for v in self.has_xrefs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Phenotype(YAMLRoot):
    """
    A phenotype is a property of an organism that can be measured or observed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/Phenotype"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/Phenotype"
    class_name: ClassVar[str] = "Phenotype"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/Phenotype")

    id: Union[str, PhenotypeId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    has_xrefs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhenotypeId):
            self.id = PhenotypeId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.display_name is not None and not isinstance(self.display_name, str):
            self.display_name = str(self.display_name)

        if not isinstance(self.has_xrefs, list):
            self.has_xrefs = [self.has_xrefs] if self.has_xrefs is not None else []
        self.has_xrefs = [v if isinstance(v, str) else str(v) for v in self.has_xrefs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Association(YAMLRoot):
    """
    An association between a gene and a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/Association"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/Association"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/Association")

    id: Union[str, AssociationId] = None
    gene: Optional[Union[str, GeneId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AssociationId):
            self.id = AssociationId(self.id)

        if self.gene is not None and not isinstance(self.gene, GeneId):
            self.gene = GeneId(self.gene)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DirectSupportAssociation(Association):
    """
    A direct support association between a gene and a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/DirectSupportAssociation"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/DirectSupportAssociation"
    class_name: ClassVar[str] = "DirectSupportAssociation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/DirectSupportAssociation")

    id: Union[str, DirectSupportAssociationId] = None
    gene: Optional[Union[str, GeneId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    score: Optional[Union[dict, "Score"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DirectSupportAssociationId):
            self.id = DirectSupportAssociationId(self.id)

        if self.gene is not None and not isinstance(self.gene, GeneId):
            self.gene = GeneId(self.gene)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if self.score is not None and not isinstance(self.score, Score):
            self.score = Score()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IndirectSupportAssociation(YAMLRoot):
    """
    An indirect support association between a gene and a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/IndirectSupportAssociation"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/IndirectSupportAssociation"
    class_name: ClassVar[str] = "IndirectSupportAssociation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/IndirectSupportAssociation")

    id: Union[str, IndirectSupportAssociationId] = None
    gene: Optional[Union[str, GeneId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    score: Optional[Union[dict, "Score"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndirectSupportAssociationId):
            self.id = IndirectSupportAssociationId(self.id)

        if self.gene is not None and not isinstance(self.gene, GeneId):
            self.gene = GeneId(self.gene)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if self.score is not None and not isinstance(self.score, Score):
            self.score = Score()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CombinedSupportAssociation(YAMLRoot):
    """
    A combined support association between a gene and a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/CombinedSupportAssociation"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/CombinedSupportAssociation"
    class_name: ClassVar[str] = "CombinedSupportAssociation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/CombinedSupportAssociation")

    id: Union[str, CombinedSupportAssociationId] = None
    gene: Optional[Union[str, GeneId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    score: Optional[Union[dict, "Score"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CombinedSupportAssociationId):
            self.id = CombinedSupportAssociationId(self.id)

        if self.gene is not None and not isinstance(self.gene, GeneId):
            self.gene = GeneId(self.gene)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if self.score is not None and not isinstance(self.score, Score):
            self.score = Score()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Gwas(YAMLRoot):
    """
    A Genome-Wide Association Study (GWAS) that has been published.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/Gwas"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/Gwas"
    class_name: ClassVar[str] = "Gwas"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/Gwas")

    id: Union[str, GwasId] = None
    description: Optional[str] = None
    name: Optional[str] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    has_xrefs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GwasId):
            self.id = GwasId(self.id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if not isinstance(self.has_xrefs, list):
            self.has_xrefs = [self.has_xrefs] if self.has_xrefs is not None else []
        self.has_xrefs = [v if isinstance(v, str) else str(v) for v in self.has_xrefs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneSet(YAMLRoot):
    """
    A set of genes that are associated. Used in PIGEAN.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/GeneSet"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/GeneSet"
    class_name: ClassVar[str] = "GeneSet"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/GeneSet")

    id: Union[str, GeneSetId] = None
    name: Optional[str] = None
    description: Optional[str] = None
    has_xrefs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneSetId):
            self.id = GeneSetId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.has_xrefs, list):
            self.has_xrefs = [self.has_xrefs] if self.has_xrefs is not None else []
        self.has_xrefs = [v if isinstance(v, str) else str(v) for v in self.has_xrefs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneSetJointEffectAssociation(Association):
    """
    The joint effect size of a gene set for a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/GeneSetJointEffectAssociation"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/GeneSetJointEffectAssociation"
    class_name: ClassVar[str] = "GeneSetJointEffectAssociation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/GeneSetJointEffectAssociation")

    id: Union[str, GeneSetJointEffectAssociationId] = None
    gene_set: Optional[Union[str, GeneSetId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    score: Optional[Union[dict, "Score"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneSetJointEffectAssociationId):
            self.id = GeneSetJointEffectAssociationId(self.id)

        if self.gene_set is not None and not isinstance(self.gene_set, GeneSetId):
            self.gene_set = GeneSetId(self.gene_set)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if self.score is not None and not isinstance(self.score, Score):
            self.score = Score()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeneSetMarginalEffectAssociation(Association):
    """
    The marginal effect size of a gene set for a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/GeneSetMarginalEffectAssociation"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/GeneSetMarginalEffectAssociation"
    class_name: ClassVar[str] = "GeneSetMarginalEffectAssociation"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/GeneSetMarginalEffectAssociation")

    id: Union[str, GeneSetMarginalEffectAssociationId] = None
    gene_set: Optional[Union[str, GeneSetId]] = None
    phenotype: Optional[Union[str, PhenotypeId]] = None
    score: Optional[Union[dict, "Score"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneSetMarginalEffectAssociationId):
            self.id = GeneSetMarginalEffectAssociationId(self.id)

        if self.gene_set is not None and not isinstance(self.gene_set, GeneSetId):
            self.gene_set = GeneSetId(self.gene_set)

        if self.phenotype is not None and not isinstance(self.phenotype, PhenotypeId):
            self.phenotype = PhenotypeId(self.phenotype)

        if self.score is not None and not isinstance(self.score, Score):
            self.score = Score()

        super().__post_init__(**kwargs)


class Score(YAMLRoot):
    """
    The strength of an association.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/Score"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/Score"
    class_name: ClassVar[str] = "Score"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/Score")


class DirectSupportScore(Score):
    """
    The direct genetic support a gene has for a trait expressed in log odds.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/DirectSupportScore"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/DirectSupportScore"
    class_name: ClassVar[str] = "DirectSupportScore"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/DirectSupportScore")


class IndirectSupportScore(YAMLRoot):
    """
    The indirect genetic support a gene has for a trait expressed in log odds.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/IndirectSupportScore"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/IndirectSupportScore"
    class_name: ClassVar[str] = "IndirectSupportScore"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/IndirectSupportScore")


class CombinedSupportScore(Score):
    """
    The combined genetic support a gene has for a trait expressed in log odds.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/CombinedSupportScore"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/CombinedSupportScore"
    class_name: ClassVar[str] = "CombinedSupportScore"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/CombinedSupportScore")


class MarginalEffectScore(Score):
    """
    The marginal effect a gene set has for a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/MarginalEffectScore"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/MarginalEffectScore"
    class_name: ClassVar[str] = "MarginalEffectScore"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/MarginalEffectScore")


class JointEffectScore(Score):
    """
    The joint effect a gene set has for a trait.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = A2F["portal-model/JointEffectScore"]
    class_class_curie: ClassVar[str] = "a2f:portal-model/JointEffectScore"
    class_name: ClassVar[str] = "JointEffectScore"
    class_model_uri: ClassVar[URIRef] = URIRef("https://w3id.org/a2f/portal-model/JointEffectScore")


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=DEFAULT_.id, name="id", curie=DEFAULT_.curie('id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.symbol = Slot(uri=DEFAULT_.symbol, name="symbol", curie=DEFAULT_.curie('symbol'),
                   model_uri=DEFAULT_.symbol, domain=None, range=Optional[str])

slots.name = Slot(uri=DEFAULT_.name, name="name", curie=DEFAULT_.curie('name'),
                   model_uri=DEFAULT_.name, domain=None, range=Optional[str])

slots.display_name = Slot(uri=DEFAULT_.display_name, name="display_name", curie=DEFAULT_.curie('display_name'),
                   model_uri=DEFAULT_.display_name, domain=None, range=Optional[str])

slots.description = Slot(uri=DEFAULT_.description, name="description", curie=DEFAULT_.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=Optional[str])

slots.gene = Slot(uri=DEFAULT_.gene, name="gene", curie=DEFAULT_.curie('gene'),
                   model_uri=DEFAULT_.gene, domain=None, range=Optional[Union[str, GeneId]])

slots.phenotype = Slot(uri=DEFAULT_.phenotype, name="phenotype", curie=DEFAULT_.curie('phenotype'),
                   model_uri=DEFAULT_.phenotype, domain=None, range=Optional[Union[str, PhenotypeId]])

slots.score = Slot(uri=DEFAULT_.score, name="score", curie=DEFAULT_.curie('score'),
                   model_uri=DEFAULT_.score, domain=None, range=Optional[Union[dict, Score]])

slots.gene_set = Slot(uri=DEFAULT_.gene_set, name="gene_set", curie=DEFAULT_.curie('gene_set'),
                   model_uri=DEFAULT_.gene_set, domain=None, range=Optional[Union[str, GeneSetId]])

slots.gene__has_xrefs = Slot(uri=DEFAULT_.has_xrefs, name="gene__has_xrefs", curie=DEFAULT_.curie('has_xrefs'),
                   model_uri=DEFAULT_.gene__has_xrefs, domain=None, range=Optional[Union[str, List[str]]])

slots.phenotype__has_xrefs = Slot(uri=DEFAULT_.has_xrefs, name="phenotype__has_xrefs", curie=DEFAULT_.curie('has_xrefs'),
                   model_uri=DEFAULT_.phenotype__has_xrefs, domain=None, range=Optional[Union[str, List[str]]])

slots.gwas__has_xrefs = Slot(uri=DEFAULT_.has_xrefs, name="gwas__has_xrefs", curie=DEFAULT_.curie('has_xrefs'),
                   model_uri=DEFAULT_.gwas__has_xrefs, domain=None, range=Optional[Union[str, List[str]]])

slots.geneSet__has_xrefs = Slot(uri=DEFAULT_.has_xrefs, name="geneSet__has_xrefs", curie=DEFAULT_.curie('has_xrefs'),
                   model_uri=DEFAULT_.geneSet__has_xrefs, domain=None, range=Optional[Union[str, List[str]]])
