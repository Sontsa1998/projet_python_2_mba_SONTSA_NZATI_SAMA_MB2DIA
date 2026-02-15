"""Exceptions personnalisées pour l'API Transaction.

Ce module définit les classes d'exception personnalisées pour l'API Transaction, fournissant
des types d'erreur spécifiques pour différents scénarios d'échec dans l'application.

Classes
-------
TransactionAPIException
    Classe d'exception de base pour toutes les exceptions de l'API Transaction.
TransactionNotFound
    Levée quand une transaction demandée ne peut pas être trouvée.
CustomerNotFound
    Levée quand un client demandé ne peut pas être trouvé.
InvalidPaginationParameters
    Levée quand les paramètres de pagination sont invalides.
InvalidSearchFilters
    Levée quand les paramètres de filtre de recherche sont invalides.
DataLoadingError
    Levée quand le chargement des données à partir du CSV échoue.
InvalidTransactionData
    Levée quand les données de transaction sont invalides ou malformées.
"""


class TransactionAPIException(Exception):
    """Exception de base pour l'API Transaction.
    
    Ceci est la classe d'exception de base pour toutes les exceptions personnalisées
    dans l'API Transaction. Toutes les autres exceptions personnalisées héritent de cette classe.
    """

    pass


class TransactionNotFound(TransactionAPIException):
    """Exception levée quand une transaction n'est pas trouvée.
    
    Cette exception est levée quand une recherche de transaction échoue parce que
    l'ID de transaction demandé n'existe pas dans le référentiel.
    """

    pass


class CustomerNotFound(TransactionAPIException):
    """Exception levée quand un client n'est pas trouvé.
    
    Cette exception est levée quand une recherche de client échoue parce que
    l'ID de client demandé n'existe pas dans le référentiel.
    """

    pass


class InvalidPaginationParameters(TransactionAPIException):
    """Exception levée quand les paramètres de pagination sont invalides.
    
    Cette exception est levée quand les paramètres de pagination (page, limit) sont
    en dehors des plages acceptables ou violent les règles de validation.
    """

    pass


class InvalidSearchFilters(TransactionAPIException):
    """Exception levée quand les filtres de recherche sont invalides.
    
    Cette exception est levée quand les paramètres de filtre de recherche sont malformés,
    contiennent des valeurs invalides ou violent les contraintes de logique métier.
    """

    pass


class DataLoadingError(TransactionAPIException):
    """Exception levée quand le chargement des données échoue.
    
    Cette exception est levée quand le chargement des données de transaction à partir du fichier CSV
    échoue en raison d'erreurs d'E/S de fichier, d'erreurs d'analyse ou d'autres problèmes de chargement de données.
    """

    pass


class InvalidTransactionData(TransactionAPIException):
    """Exception levée quand les données de transaction sont invalides.
    
    Cette exception est levée quand les données de transaction sont malformées, manquent de champs requis,
    ou contiennent des valeurs qui violent les règles de validation des données.
    """

    pass
