from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class MatchStatus(Enum):
    suspendu = "suspendu"
    annule = "annule"
    en_direct = "en_direct"
    pause = "pause"
    reporte = "reporte"
    a_venir = "a_venir"
    termine = "termine"

class Surface(Enum):
    gazon = "gazon"
    dur_outdoor = "dur_outdoor"
    dur_indoor = "dur_indoor"
    moquette = "moquette"
    terre_battue = "terre_battue"
    beton = "beton"

class NotificationType(Enum):
    break_realise_tennis = "break_realise_tennis"
    match_commence = "match_commence"
    match_termine = "match_termine"
    but_marque_football = "but_marque_football"
    nouveau_message = "nouveau_message"
    essai_marque_rugby = "essai_marque_rugby"
    demande_ami = "demande_ami"
    set_gagne_tennis = "set_gagne_tennis"
    invitation_canal = "invitation_canal"

class SportType(Enum):
    football = "football"
    tennis = "tennis"
    rugby = "rugby"

class MatchType(Enum):
    simple = "simple"
    double_mixte = "double_mixte"
    equipes = "equipes"
    double = "double"

class ReactionType(Enum):
    choc = "choc"
    rire = "rire"
    triste = "triste"
    coeur = "coeur"
    colere = "colere"
    feu = "feu"
    pouce_haut = "pouce_haut"

class UserRole(Enum):
    user = "user"
    admin = "admin"
    moderateur = "moderateur"

class LineupStatus(Enum):
    provisoire = "provisoire"
    annulee = "annulee"
    officielle = "officielle"

class MatchEventType(Enum):
    break_tennis = "break_tennis"
    transformation = "transformation"
    faute = "faute"
    carton_jaune = "carton_jaune"
    set_gagne = "set_gagne"
    drop = "drop"
    but = "but"
    hors_jeu = "hors_jeu"
    autre = "autre"
    jeu_gagne = "jeu_gagne"
    carton_rouge = "carton_rouge"
    mele_accordee = "mele_accordee"
    penalty = "penalty"
    tie_break = "tie_break"
    ace = "ace"
    remplacement = "remplacement"
    double_faute = "double_faute"
    essai = "essai"

class CompetitionStatus(Enum):
    termine = "termine"
    en_cours = "en_cours"
    suspendue = "suspendue"
    a_venir = "a_venir"

class PositionType(Enum):
    ailier = "ailier"
    milieu = "milieu"
    attaquant = "attaquant"
    demi_de_melee = "demi_de_melee"
    pilier = "pilier"
    ouvreur = "ouvreur"
    talonneur = "talonneur"
    autre = "autre"
    centre = "centre"
    deuxieme_ligne = "deuxieme_ligne"
    defenseur = "defenseur"
    arriere = "arriere"
    troisieme_ligne = "troisieme_ligne"
    gardien = "gardien"

class FriendshipStatus(Enum):
    accepte = "accepte"
    en_attente = "en_attente"
    refuse = "refuse"
    bloque = "bloque"

class ChannelType(Enum):
    match = "match"
    groupe_amis = "groupe_amis"
    competition = "competition"

class CompetitionFormat(Enum):
    championnat = "championnat"
    coupe = "coupe"
    tournoi = "tournoi"
    phase_groupes_puis_tournoi = "phase_groupes_puis_tournoi"

############################################
# Classes are defined here
############################################
class TennisSetCreate(BaseModel):
    id: str
    jeux_j2: int
    gagnant_id: Optional[str] = None
    numero_set: int
    tb_points_j1: Optional[int] = None
    est_termine: bool
    jeux_j1: int
    tb_points_j2: Optional[int] = None
    match: int  # N:1 Relationship (mandatory)


class MatchPreviewCreate(BaseModel):
    forme_exterieur: Optional[str] = None
    h2h_victoires_ext: Optional[int] = None
    id: str
    enjeu: Optional[str] = None
    h2h_victoires_dom: Optional[int] = None
    absents_domicile: Optional[str] = None
    forme_domicile: Optional[str] = None
    publie_le: datetime
    h2h_nuls: Optional[int] = None
    absents_exterieur: Optional[str] = None
    match: int  # 1:1 Relationship (mandatory)


class TeamCreate(BaseModel):
    abreviation: str
    nom: str
    ville: str
    id: str
    pays: str
    logo_url: str
    stade: str
    evenements_equipe: Optional[List[int]] = None  # 1:N Relationship
    competitions: Optional[List[int]] = None  # N:M Relationship (optional)
    joueurs: Optional[List[int]] = None  # 1:N Relationship
    classements: Optional[List[int]] = None  # 1:N Relationship
    lineups: Optional[List[int]] = None  # 1:N Relationship
    stade_domicile: Optional[int] = None  # N:1 Relationship (optional)
    matchs_a_domicile: Optional[List[int]] = None  # 1:N Relationship
    matchs_a_exterieur: Optional[List[int]] = None  # 1:N Relationship
    fans: Optional[List[int]] = None  # 1:N Relationship


class StandingCreate(BaseModel):
    classement: int
    id: str
    points_concedes: int
    points: int
    defaites: int
    matchs_joues: int
    points_marques: int
    victoires: int
    difference_points: int
    nuls: int
    competition: int  # N:1 Relationship (mandatory)
    equipe: int  # N:1 Relationship (mandatory)


class PreMatchOddsCreate(BaseModel):
    id: str
    pct_victoire_ext: float
    pct_victoire_dom: float
    source: str
    pct_match_nul: Optional[float] = None
    updated_at: datetime
    match: int  # 1:1 Relationship (mandatory)


class SportCreate(BaseModel):
    id: str
    logo_url: str
    description: str
    nom: str
    type: SportType
    competitions: Optional[List[int]] = None  # 1:N Relationship


class LineupPlayerCreate(BaseModel):
    position_match: str
    est_capitaine: bool
    numero_maillot: Optional[int] = None
    ordre_entree: Optional[int] = None
    id: str
    est_titulaire: bool
    joueur: int  # N:1 Relationship (mandatory)
    lineup: int  # N:1 Relationship (mandatory)


class ReactionCreate(BaseModel):
    type: ReactionType
    id: str
    created_at: datetime
    user: int  # N:1 Relationship (mandatory)
    message: int  # N:1 Relationship (mandatory)


class LineupCreate(BaseModel):
    statut: LineupStatus
    id: str
    role_double: Optional[str] = None
    publiee_le: Optional[datetime] = None
    formation: Optional[str] = None
    est_domicile: bool
    joueurs: Optional[List[int]] = None  # 1:N Relationship
    equipe: int  # N:1 Relationship (mandatory)
    match: int  # N:1 Relationship (mandatory)


class PlayerCreate(BaseModel):
    nom: str
    prenom: str
    id: str
    numero: int
    nationalite: str
    date_naissance: datetime
    photo_url: str
    position: PositionType
    apparitions: Optional[List[int]] = None  # 1:N Relationship
    joueur: int  # N:1 Relationship (mandatory)
    evenements_joues: Optional[List[int]] = None  # 1:N Relationship
    equipe: int  # N:1 Relationship (mandatory)


class StadiumCreate(BaseModel):
    id: str
    longitude: Optional[float] = None
    pays: str
    photo_url: Optional[str] = None
    nom: str
    capacite: Optional[int] = None
    latitude: Optional[float] = None
    ville: str
    pelouse: Optional[str] = None
    equipes_domicile: Optional[List[int]] = None  # 1:N Relationship
    matchs: Optional[List[int]] = None  # 1:N Relationship


class NotificationCreate(BaseModel):
    created_at: datetime
    titre: str
    type: NotificationType
    id: str
    contenu: str
    is_read: bool
    user: int  # N:1 Relationship (mandatory)


class MediaFileCreate(BaseModel):
    id: str
    alt_text: Optional[str] = None
    uploaded_by: str
    mimetype: str
    url: str
    cible_type: str
    created_at: datetime
    cible_id: str
    taille_ko: Optional[int] = None
    filename: str
    uploader: Optional[int] = None  # N:1 Relationship (optional)


class MessageCreate(BaseModel):
    edited_at: datetime
    minute_match: int
    content: str
    id: str
    created_at: datetime
    is_deleted: bool
    auteur: int  # N:1 Relationship (mandatory)
    reactions: Optional[List[int]] = None  # 1:N Relationship
    reponses: Optional[List[int]] = None  # 1:N Relationship
    parent: Optional[int] = None  # N:1 Relationship (optional)
    canal: int  # N:1 Relationship (mandatory)


class BracketSlotCreate(BaseModel):
    equipe_exterieur_id: Optional[str] = None
    position: int
    vainqueur_id: Optional[str] = None
    equipe_domicile_id: Optional[str] = None
    est_qualifie: Optional[bool] = None
    id: str
    tour: int  # N:1 Relationship (mandatory)
    match: int  # 1:1 Relationship (mandatory)


class MatchEventCreate(BaseModel):
    type: MatchEventType
    description: str
    id: str
    created_at: datetime
    minute: int
    equipe: Optional[int] = None  # N:1 Relationship (optional)
    joueur: Optional[int] = None  # N:1 Relationship (optional)
    match: int  # N:1 Relationship (mandatory)


class TournamentRoundCreate(BaseModel):
    date_debut: datetime
    nom: str
    date_fin: Optional[datetime] = None
    statut: Optional[CompetitionStatus] = None
    numero: int
    id: str
    slots: Optional[List[int]] = None  # 1:N Relationship
    competition: int  # N:1 Relationship (mandatory)


class MatchCreate(BaseModel):
    score_jeu_actuel: Optional[str] = None
    type_match: MatchType
    status: MatchStatus
    progression: Optional[str] = None
    created_at: datetime
    surface: Optional[Surface] = None
    journee: Optional[int] = None
    serveur_id: Optional[str] = None
    updated_at: datetime
    score_domicile: int
    date_heure: datetime
    set_actuel: Optional[int] = None
    lieu: str
    tour_tournoi: Optional[str] = None
    score_exterieur: int
    id: str
    compositions: Optional[List[int]] = None  # 1:N Relationship
    stade: Optional[int] = None  # N:1 Relationship (optional)
    slot: Optional[int] = None  # 1:1 Relationship (optional)
    equipe_domicile: int  # N:1 Relationship (mandatory)
    competition: int  # N:1 Relationship (mandatory)
    canaux: Optional[List[int]] = None  # 1:N Relationship
    evenements: Optional[List[int]] = None  # 1:N Relationship
    equipe_exterieure: int  # N:1 Relationship (mandatory)
    statistiques: Optional[int] = None  # 1:1 Relationship (optional)
    sets: Optional[List[int]] = None  # 1:N Relationship
    preview: Optional[int] = None  # 1:1 Relationship (optional)
    cotes: Optional[int] = None  # 1:1 Relationship (optional)


class FriendshipCreate(BaseModel):
    id: str
    updated_at: datetime
    created_at: datetime
    status: FriendshipStatus
    demandeur: int  # N:1 Relationship (mandatory)
    receveur: int  # N:1 Relationship (mandatory)


class FavoritePlayerCreate(BaseModel):
    added_at: datetime
    notify_match: bool
    id: str
    fans: Optional[List[int]] = None  # 1:N Relationship
    user: int  # N:1 Relationship (mandatory)


class FavoriteTeamCreate(BaseModel):
    notify_match: bool
    id: str
    notify_but: bool
    added_at: datetime
    user: int  # N:1 Relationship (mandatory)
    equipe: int  # N:1 Relationship (mandatory)


class MatchStatisticsCreate(BaseModel):
    transformations_exterieur: Optional[int] = None
    breaks_j1: Optional[int] = None
    tirs_exterieur: Optional[int] = None
    penalties_dom: Optional[int] = None
    breaks_j2: Optional[int] = None
    tirs_cadres_domicile: Optional[int] = None
    penalties_ext: Optional[int] = None
    sets_j1: Optional[int] = None
    tirs_cadres_exterieur: Optional[int] = None
    meles_gagnees_dom: Optional[int] = None
    sets_j2: Optional[int] = None
    corners_domicile: Optional[int] = None
    meles_gagnees_ext: Optional[int] = None
    corners_exterieur: Optional[int] = None
    aces_j1: Optional[int] = None
    fautes_domicile: Optional[int] = None
    aces_j2: Optional[int] = None
    fautes_exterieur: Optional[int] = None
    id: Optional[str] = None
    doubles_fautes_j1: Optional[int] = None
    sport_type: Optional[SportType] = None
    essais_domicile: Optional[int] = None
    doubles_fautes_j2: Optional[int] = None
    possession_domicile: Optional[int] = None
    essais_exterieur: Optional[int] = None
    pct_premier_service_j1: Optional[int] = None
    possession_exterieur: Optional[int] = None
    transformations_domicile: Optional[int] = None
    pct_premier_service_j2: Optional[int] = None
    tirs_domicile: Optional[int] = None
    match: int  # 1:1 Relationship (mandatory)


class FavoriteCompetitionCreate(BaseModel):
    id: str
    notif_active: bool
    added_at: datetime
    created_at: datetime
    user: int  # N:1 Relationship (mandatory)
    competition: int  # N:1 Relationship (mandatory)


class UserCreate(BaseModel):
    username: str
    bio: str
    role: UserRole
    id: str
    created_at: datetime
    mot_de_passe_hash: str
    avatar_url: str
    email: str
    equipes_favorites: Optional[List[int]] = None  # 1:N Relationship
    competitions_favorites: Optional[List[int]] = None  # 1:N Relationship
    medias: Optional[List[int]] = None  # 1:N Relationship
    reactions: Optional[List[int]] = None  # 1:N Relationship
    canaux_rejoints: Optional[List[int]] = None  # 1:N Relationship
    joueurs_favoris: Optional[List[int]] = None  # 1:N Relationship
    demandes_envoyees: Optional[List[int]] = None  # 1:N Relationship
    demandes_recues: Optional[List[int]] = None  # 1:N Relationship
    notifications: Optional[List[int]] = None  # 1:N Relationship
    messages: Optional[List[int]] = None  # 1:N Relationship


class CompetitionCreate(BaseModel):
    logo_url: str
    saison: str
    date_fin: datetime
    format: CompetitionFormat
    nom: str
    statut: CompetitionStatus
    id: str
    pays: str
    date_debut: datetime
    equipes: Optional[List[int]] = None  # N:M Relationship (optional)
    classement: Optional[List[int]] = None  # 1:N Relationship
    sport: int  # N:1 Relationship (mandatory)
    matchs: Optional[List[int]] = None  # 1:N Relationship
    tours: Optional[List[int]] = None  # 1:N Relationship
    abonnes: Optional[List[int]] = None  # 1:N Relationship


class ChannelMemberCreate(BaseModel):
    is_admin: bool
    last_read_at: datetime
    id: str
    joined_at: datetime
    user: int  # N:1 Relationship (mandatory)
    canal: int  # N:1 Relationship (mandatory)


class ChannelCreate(BaseModel):
    type: ChannelType
    id: str
    is_live: bool
    created_at: datetime
    nom: str
    membres: Optional[List[int]] = None  # 1:N Relationship
    match: Optional[int] = None  # N:1 Relationship (optional)
    messages: Optional[List[int]] = None  # 1:N Relationship


