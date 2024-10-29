import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
    "Donnez-moi un résumé du rapport ",
    "Quels sont les principaux versements effectués au titre des charges communes ?",        
    "Quelle est la répartition des dépenses liées aux régimes de retraite gérés par la CMR ?",        
    "Quelles mesures d'accompagnement ont été mises en place pour soutenir les consommateurs ?",
    "Comment les dépenses pour le financement des infrastructures sportives sont-elles justifiées dans le rapport ?"
]
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()
def main():
    text=r"""
     
INTRODUCTION

Conformément à la loi organique n° 130-13 relative à la loi de finances, le budget des Charges
Communes, faisant partie intégrante du budget général, englobe les dépenses qui ne peuvent
être imputées sur les budgets des départements ministériels ou institutions.

Ce budget prend en charge certaines opérations urgentes ou revêtant un caractère d’intérêt
général, n’ayant pas fait l’objet d’une programmation préalable, et couvre des dépenses
afférentes au règlement des créances ou à l’apurement des dettes de divers établissements et
entreprises publics.

Le budget des Charges Communes se compose des crédits budgétaires programmés dans le
cadre de la loi de finances, augmentés, le cas échéant, des crédits supplémentaires ouverts
par décret en cours d'année budgétaire, des crédits prélevés sur le chapitre des Dépenses
Imprévues et Dotations Provisionnelles, des crédits ouverts par arrêté du Ministre des
Finances suite aux versements effectués au profit du budget général, à partir d'un compte
d'affectation spéciale (CAS) ou d'un service de l’Etat géré de manière autonome (SEGMA)
ainsi que des fonds de concours.

Les    crédits     programmés0            en    2024      au    titre   des        chapitres   de   fonctionnement     et
d'investissement des Charges Communes s’élèvent,                              respectivement,       à   34.820   MDH   et
43.912 MDH contre 42.104,40 MDH et 40.374,37 MDH en 2023, enregistrant, respectivement,
une baisse de près de 17% et une augmentation d’environ 9%.

En outre, les crédits de fonctionnement et d’investissement prévus au titre du budget des
Charges Communes par le projet de loi de finances pour l’année 2025, se chiffrent à
48.112 MDH et 43.602 MDH, en hausse, respectivement, d’environ 38% et 20% par rapport aux
crédits ouverts par la loi de finances pour l’année 2024.

CHAPITRE I - LE BUDGET DE FONCTIONNEMENT DES
CHARGES COMMUNES: INSTRUMENT D’ASSISTANCE
ET D’APPUI AUX POLITIQUES SOCIALES

Les   crédits     du      chapitre des Charges Communes - Fonctionnement se caractérisent par la
prépondérance des dépenses à caractère social qui concernent, essentiellement, la couverture
de la charge de compensation, y compris les mesures d’accompagnement et de soutien
relatifs au secteur du transport routier, les régimes de retraite gérés par la Caisse Marocaine
des Retraites (CMR), ainsi que la contribution au financement du chantier de généralisation de
la protection sociale.

1.1. PREVISIONS ET REALISATIONS DU CHAPITRE DE FONCTIONNEMENT
DES CHARGES COMMUNES AU TITRE DES ANNEES 2023 ET 2024
1.1.1. Réalisations au titre de Pannée 2023
Le montant des crédits ouverts au titre du chapitre de fonctionnement des Charges
Communes pour l’année 2023, s’élève à 42.104,40 MDH, compte tenu d’une somme de
3.430 MDH représentant les crédits supplémentaires ouverts par décret et destinés à faire
face aux répercussions de l'inflation sur le pouvoir d'achat des citoyens (3.300 MDH) et à
mettre en œuvre la feuille de route stratégique du tourisme 2023-2026 dans son volet
fonctionnement (130 MDH).

En outre, des crédits supplémentaires d’un montant global de 17.000 MDH ont été ouverts,
par arrêté du Ministre des Finances, en cours d’année, au niveau dudit chapitre, correspondant
aux versements effectués à partir des CAS intitulés « Fonds de remploi domanial » (14.500
MDH), « Fonds de solidarité des assurances » (1.500 MDH), et « Fonds spécial pour la gestion
de la pandémie du Coronavirus "Le Covid-19"» (1.000 MDH), D’autres crédits supplémentaires
issus de prélèvements sur le chapitre des dépenses imprévues et dotations provisionnelles
(DI) ont, également, été ouverts par décret pour un montant de 416,55 MDH.

Ces crédits ont été destinés, principalement, à la couverture d’une partie de la charge de
compensation au titre de l’année 2023 (13.000 MDH) et au financement du chantier de
généralisation de la protection sociale (4.000 MDH).

Au 31/12/2023, les engagements de dépenses au niveau du chapitre des Charges Communes -
Fonctionnement ont atteint 59.230,07 MDH, en tenant compte des crédits supplémentaires
ouverts, soit un taux d’exécution de 99,51%.

La répartition des versements effectués, au titre de l’année 2023, dans le cadre du chapitre
susvisé, se présente comme suit :



                                                      Déblocages
                                                                          Déblocages
                                                        effectués                                       Part dans le
                                                                           effectués
                                                    (par imputation                         Total des    total des
                 Opérations                                            (par prélèvement
                                                   sur le budget des                       déblocages   déblocages
                                                                         sur les crédits
                                                         Charges                                          (en %)
                                                                       supplémentaires)
                                                      Communes)

1)-Soutien aux prix à la consommation et
                                                      26.191,04           13.000,00        39.191,04      66,17%
mesures d’accompagnement

2)-Versements au      profit   des     comptes
                                                       1.741,82           4.000,00          5.741,82      9,69%
spéciaux du Trésor

3)-Dépenses liées aux régimes de retraite                                      -
                                                       4.404,71                            4.404,71       7,44%
gérés par la CMR
4)-Liquidations   au    titre   du   droit
d’importation et de la TVA à l’importation
applicables aux ovins domestiques et au
                                                        93,86              1.601,36         1.695,22      2,86%
lait écrémé en poudre, ainsi que la TVA à
l’importation   applicable    aux   bovins
domestiques
5)-Soutien            de    l’opération
d’approvisionnement du marché intérieur                    -               960,00           960,00        1,62%
en aliments de bétail

6)-Versement au profit du Crédit Agricole                  -               500,00           500,00        0,84%
du Maroc (CAM)

7)-Pensions exceptionnelles, supplément de
pensions et allocation spéciale en cas de              326,86                  -            326,86        0,55%
décès

8)-Règlement de la 5eme annuité du loyer dû
par l’Académie Régionale d’Education et de
Formation (AREF) de            la région de                                    -
                                                        216,49                              216,49        0,37%
Casablanca-Settat, à la société Maghreb
Titrisation, au titre des certificats de Sukuk
Ijara

9)-Financement         de            l’opération           -               205,46           205,46        0,35%
d’importation des ovins

10)-Versement, au profit de la SNRT, de la
2eme    tranche     de     la    subvention
exceptionnelle destinée au financement des             200,00                  -            200,00        0,34%
dépenses liées à la couverture des grands
évènements sportifs

ll)-Versement au profit de la Fondation
Mohammed VI des Sciences et de la Santé,
pour permettre à ladite fondation de                   164,00                  -            164,00        0,28%
couvrir son déficit d’exploitation enregistré
à fin 2023

12)-Règlement du coût du transfert à la
CNRA de la gestion des dossiers des ex­
employés des Charbonnages du Maroc
(CDM) victimes d’accidents du travail ou de                                    -
                                                        135,74                              135,74        0,23%
maladies    professionnelles,   des    frais
engagés par ladite Caisse dans la gestion
desdits dossiers et de l’avance stipulée
dans la convention du 28 mai 2004



                                                      Déblocages
                                                                          Déblocages
                                                        effectués                                       Part dans le
                                                                           effectués
                                                    (par imputation                         Total des    total des
                   Opérations                                          (par prélèvement
                                                   sur le budget des                       déblocages   déblocages
                                                                         sur les crédits
                                                         Charges                                          (en %)
                                                                       supplémentaires)
                                                      Communes)

13)-Règlement  de    la   subvention   de
fonctionnement accordée à l’Agence pour                103,00                  -            103,00        0,17%
('Aménagement de la Vallée du Bouregreg

14)-Autres dépenses                                   4.924,67             461,05          5.385,72       9,09%


                     Total                            38.502,19           20.727,87        59.230,07      100%



1.1.2. Crédits alloués et réalisations au titre de la période allant du 1er
janvier au 1er juin 2024
Le montant des crédits inscrits au chapitre de fonctionnement des Charges Communes pour
l’année 2024, s’élève à 34.820 MDH.

Au 1er juin 2024, les crédits engagés au titre dudit chapitre ont atteint 12.189,47 MDH, soit un
taux d’exécution de 35,01%.

Les versements effectués’ jusqu’à cette date, dans le cadre du chapitre susvisé, sont ventilés
comme suit :
                                                      Déblocages
                                                                          Déblocages
                                                        effectués                                       Part dans le
                                                                           effectués
                                                    (par imputation                         Total des    total des
                   Opérations                                          (par prélèvement
                                                   sur le budget des                       déblocages   déblocages
                                                                         sur les crédits
                                                         Charges                                          (en %)
                                                                       supplémentaires)
                                                      Communes)

1)-Soutien aux prix à la consommation et
                                                      4.559,00                 -           4.559,00      37,40%
mesures d’accompagnement

2)-Dépenses liées aux régimes de retraite
                                                       3.841,94                -            3.841,94      31,52%
gérés par la CMR

3)-Versements au          profit   des   comptes
                                                        471,22                 -             471,22       3,87%
spéciaux du Trésor
4)-Liquidations    au    titre   du     droit
d’importation et de la taxe sur la valeur
ajoutée à l’importation applicables aux
                                                       304,87                  -            304,87        2,50%
ovins domestiques, et au titre de la taxe sur
la valeur ajoutée à l’importation applicable
aux bovins domestiques
5)-Pensions exceptionnelles, supplément de
pensions et allocation spéciale en cas de              232,46                  -            232,46         1,91%
décès




 En millions de Dirhams
                                           



                                                    Déblocages
                                                                             Déblocages
                                                      effectués                                              Part dans le
                                                                              effectués
                                                  (par imputation                                Total des    total des
                 Opérations                                               (par prélèvement
                                                 sur le budget des                              déblocages   déblocages
                                                                            sur les crédits
                                                       Charges                                                 (en %)
                                                                          supplémentaires)
                                                    Communes)
6)-Versement au profit de la Société
Nationale    de    Radiodiffusion   et   de
Télévision (SNRT), au titre de la mise en
oeuvre des engagements en termes de                  146,70                       -               146,70       1,20%
couverture    en     direct   des    grands
évènements      sportifs  continentaux   et
mondiaux

7)-Autres dépenses                                   2.633,28                     -              2.633,28      21,60%


                   Total                            12.189,47                     -              12.189,47     100%




1.2. REPARTITION DES CREDITS DE FONCTIONNEMENT AU TITRE DE
L’ANNEE 2023 ET DE LA PERIODE ALLANT DU 1er JANVIER AU 1er JUIN
2024
1.2.1. Charge de compensation
Les crédits mobilisés dans le cadre du chapitre de fonctionnement des Charges Communes,
au titre de la couverture de la charge de compensation et de la prise en charge de l'impact
des mesures d'accompagnement, durant l’année 2023 et la période allant du 1er janvier au
1er juin 2024, sont présentés dans le tableau ci-après :
                                                                                                               (en MDH)

                                                                                              2023            2024°


-Soutien aux prix à la consommation :                                                    36.605,04           3.009,00

  • Compensation du gaz butane                                                           21.700,00           2.000,00

  • Compensation de la farine nationale et du blé tendre                                  7.050,00           480,00

  • Compensation du sucre                                                                 4.530,00           500,00

  • Subvention additionnelle au sucre brut à l'importation                                3.020,00               -

  • Subvention du sucre et de l'huile destinés aux provinces sahariennes                      176,00          20,00
  • Versement d'une subvention forfaitaire des prix des manuels scolaires
    destinés à l'enseignement primaire et secondaire collégial produits                       103,47             -
    localement au cours de l'année 2023
  • Dispositif compensatoire au profit des industriels opérant dans le secteur                16,57              -
    de la biscuiterie en 2022

  • Frais de gestion des dépôts et de             manutention        de    l'activité         5,00             5,00
    d'approvisionnement des Provinces du Sud

  • Versement des fonds relatifs à l'approvisionnement de la population des                   4,00             4,00
    nécessiteux des provinces du sud





                                                                                  2023       2024°


  -Mesures d’accompagnement :                                                   2.586,00    1.550,00

  • Versement de l'aide directe exceptionnelle servie au secteur du transport   2.500,00     1.550,00
    routier

  • Couverture des dépenses afférentes au transport urbain par autobus           86,00           -

                                        TOTAL                                   39.191,04   4.559,00

       Au 1er juin 2024.


1.2.2. Dépenses liées aux régimes de retraite gérés par la CMR
Le budget de fonctionnement des Charges Communes prend, également, en charge certaines
dépenses liées aux régimes de retraite gérés par la CMR, telles que le déficit du régime des
pensions militaires, les allocations familiales des pensionnés, l’impact du relèvement de la
pension minimale ainsi que les dépenses des régimes non contributifs.

Le tableau ci-après décline les principaux versements effectués au titre desdites dépenses, au
cours de l’année 2023 et de la période allant du 1er janvier au 1er juin 2024 :
                                                                                               (en MDH)

                                                                                  2023       2024°

 Couverture du déficit du régime des pensions militaires                        2.050,00    2.316,02(-)

-Prise en charge des allocations familiales des retraités :                      803,83      573,98

              • Régime des pensions civiles                                      382,00       180,25

              • Régime des pensions militaires                                   409,00       387,50

              • Régimes non contributifs                                          12,83        6,23
-Couverture des dépenses des régimes non contributifs :                          651,03       313,52

              • Pensions d’invalidité                                            502,71      246,05

              • Pensions et allocations des résistants                           145,70       66,26

              • Autres régimes non contributifs                                   2,62         1,21
-Prise en charge de l’impact du relèvement de la pension minimale                503,02      254,02
-Règlement du montant du rappel des pensions à servir au 31/12/2019, ainsi
que les intérêts y afférents, pour les retraités du Ministère chargé de          384,40      384,40
l’Education Nationale
-Couverture des frais de gestion des régimes non contributifs                     12,43          -

                                        TOTAL                                   4.404,71    3.841,94

       Au 1er juin 2024.
       Crédits engagés au titre de l’année 2024.
                                      NOTE SUR LES DEPENSES RELATIVES AUX CHARGES COMMUNES



1.2.3. Dépenses et charges diverses
Ces dépenses portent, essentiellement, sur

 •   Les versements effectués au profit du Fonds d’appui à la protection sociale et à la
     cohésion sociale pour le financement du chantier de la généralisation de la protection
     sociale (4.400 MDH en 2023) ;

 •   Les paiements au profit d’autres comptes spéciaux du Trésor, en l’occurrence les CAS
     intitulés « Financement des dépenses d’équipement et de la lutte contre le chômage »,
     « Fonds de lutte contre les effets des catastrophes naturelles », « Fonds spécial pour le
     soutien des établissements pénitentiaires », « Fonds de soutien à la sûreté nationale »,
     « Fonds national pour l'action culturelle », « Fonds de développement agricole » et
     « Fonds pour la promotion du paysage audiovisuel et des annonces et de l’édition
     publique » (1.341,82 MDH en 2023 et 471,22 MDH au 1er juin 2024) ;

 •   Les charges afférentes aux pensions et allocations diverses (366,86 MDH en 2023 et
     232,46 MDH au 1er juin 2024) ;

 •   Le loyer dû par l’Académie Régionale d’Education et de Formation (AREF) de la Région
     de Casablanca-Settat, à la société Maghreb Titrisation, au titre des certificats de Sukuk
     Ijara (216,49 MDH en 2023).

CHAPITRE II - LE BUDGET D’INVESTISSEMENT DES
CHARGES COMMUNES : INSTRUMENT D’APPUI A LA
MISE EN ŒUVRE DES STRATEGIES SECTORIELLES ET
DES PROJETS STRUCTURANTS

Les    crédits   du    chapitre    d’investissement     des   Charges    Communes       sont     destinés,
principalement, aux transferts au           profit de certains comptes spéciaux du Trésor et
établissements et entreprises publics, ainsi qu’au règlement de la contribution du Ministère
de l’Economie et des Finances au financement de différents projets structurants à caractère
économique et social.

11.1. PREVISIONS ET REALISATIONS DU CHAPITRE D’INVESTISSEMENT
DES CHARGES COMMUNES AU TITRE DES ANNEES 2023 ET 2024
11.1.1. Réalisations au titre de l’année 2023
Le montant des crédits programmés au titre du chapitre d’investissement des Charges
Communes pour l’année 2023, s’élève à 40.374,37 MDH, en tenant compte des crédits
supplémentaires d’un montant de 6.570 MDH ouverts par décret et destinés à l’ONEE sous
forme de fonds de dotation (4.000 MDH), au financement du programme national pour
l'approvisionnement en eau potable et l'irrigation pour la période 2020-2027 (1.500 MDH),
ainsi qu’à la couverture des dépenses afférentes à la mise en oeuvre de la feuille de route
stratégique du tourisme 2023-2026 dans son volet investissement (1.070 MDH).

Par ailleurs, les crédits ouverts au titre dudit chapitre ont été augmentés d’un montant de
12.622,92   MDH       suite à   l’ouverture,   par arrêté du     Ministre des    Finances,     de crédits
supplémentaires correspondant aux versements effectués à partir des CAS intitulés « Fonds
de remploi domanial » (6.722,92 MDH), « Fonds de solidarité des assurances » (3.000 MDH),
« Fonds de solidarité interrégionale » (1.000 MDH), « Part des collectivités territoriales dans
le produit de la T.V.A » (1.000 MDH) et « Fonds d’entraide familiale (900 MDH).

Ces    crédits   supplémentaires      ont   été   destinés,   essentiellement,   au   financement     des
opérations ci-après :

   •   Versement au CAS : « Fonds spécial pour la gestion des effets du tremblement de
       terre ayant touché le Royaume du Maroc » (5.900 MDH) ;

   •   Versement au CAS : « Fonds national du développement du sport» (2.000 MDH) ;

   •   Versement, au profit de l’ONCF, de la 3eme tranche de la dotation en capital de l’Etat
        pour l’année 2023 (1.000 MDH) ;

   •   Financement des projets de renforcement de l’approvisionnement en eau potable de
        la région de Casablanca - Settat (1.000 MDH) ;



      •     Règlement du reliquat de la contribution du Ministère de l’Economie et des Finances
            destinée au financement du programme de relogement des ménages issus des
            bidonvilles de la préfecture de Skhirate-Temara (543,42 MDH) ;

      •     Financement du programme de réalisation des zones d'activités économiques dédiées
            aux unités de production identifiées à risque et nécessitant une délocalisation au
            niveau de la ville de Casablanca et de ses environs (200 MDH).

A      la   fin   de    l’exercice      budgétaire    2023,       les   crédits    engagés      au     titre    du    chapitre
d’investissement des Charges Communes se chiffrent à 52.974,08 MDH, compte tenu des
crédits supplémentaires ouverts, soit un taux d’exécution d’environ 99,96%.

Les principaux versements effectués’, au titre de l’année 2023, dans le cadre du chapitre
susvisé, se déclinent comme suit :

                                                         Déblocages
                                                                               Déblocages
                                                           effectués                                                 Part dans le
                                                                                effectués
                                                       (par imputation                            Total des           total des
                       Opérations                                           (par prélèvement
                                                      sur le budget des                          déblocages          déblocages
                                                                              sur les crédits
                                                           Charges                                                     (en %)
                                                                            supplémentaires)
                                                         Communes)
“□-Versements au             profit   des   comptes
                                                         23.335,81             9.400,00          32.735,81             61,80%
spéciaux du Trésor

2)-Versement au profit de l’ONEE, sous                        -                4.000,00          4.000,00              7,55%
forme de dotation en capital
3)-Versement, au profit de l’ONCF, de la
dotation en capital de l’Etat pour l’année                600,00                  1.000,00       1.600,00              3,02%
2023
4)-Versement au profit de la Compagnie
Nationale Royal Air Maroc, sous forme d’un               1.500,00                    -           1.500,00              2,83%
apport en capital
5)-Financement et opérationnalisation du
programme « FORSA » au titre de l’année                   1.150,00                   -               1.150,00           2,17%
2023
6)-Financement     des     projets    de
renforcement de l’approvisionnement en                        -                   1.000,00       1.000,00              1,89%
eau potable de la région de Casablanca -
Settat
7)-Règlement, au profit de l’ONMT, de la
contribution de l’Etat prévue par la
convention spécifique pour le déploiement                     -                   750,00             750,00            1,42%
de la feuille de route stratégique du
secteur du tourisme

8)-Financement du            programme
d’investissement triennal 2021-2023 de
l’Agence pour l’Aménagement de la Vallée                  630,00                                     630,00             1,19%
du Bouregreg et des projets engagés par
ladite agence




*
    En millions de Dirhams





                                                  Déblocages
                                                                      Déblocages
                                                    effectués                                       Part dans le
                                                                       effectués
                                                (par imputation                         Total des    total des
                 Opérations                                        (par prélèvement
                                               sur le budget des                       déblocages   déblocages
                                                                     sur les crédits
                                                    Charges                                           (en %)
                                                                   supplémentaires)
                                                  Communes)
9)-Règlement     du     reliquat   de   la
contribution du Ministère de l’Economie et
des Finances destinée au financement du                -               543,42           543,42        1,04%
programme de relogement des ménages
issus des bidonvilles de la préfecture de
Skhirate-T emara
10)-Règlement de la 2eme tranche de la part
de l'Etat dans l'augmentation du capital du        500,00                  -            500,00        0,94%
CAM
ll)-Couverture du gap constaté au titre de
l’exercice 2022 et des trois premiers
trimestres de l’année 2023, résultant du
différentiel du coût de l’eau potable                                      -
                                                   441,50                               441,50        0,83%
destinée à l’alimentation de la zone du
Grand Agadir provenant de l’unité de
dessalement d’eau de mer de la province
de Chtouka Ait Baha
12)-Règlement, au profit de la Société
Marocaine d’ingénierie Touristique (SMIT),
de la contribution de l'Etat au titre de la                                -
                                                   400,00                               400,00        0,76%
convention d'appui pour la mise à niveau
des      établissements     d'hébergement
touristique
13)-Prise en charge du        crédit TVA de                                -
                                                   387,37                               387,37        0,73%
l’ONEE

14)- Prise en charge du crédit TVA de                                      -
                                                    318,04                              318,04        0,60%
l’ONCF
15)-Versements au profit de l’ONHYM, au
titre du financement de l’acquisition du
Gaz technique stocké au niveau du                                          -
                                                    301,50                              301,50        0,57%
Gazoduc Maghreb Europe (GME) et de la
phase pré-FID du Projet Stratégique du
Gazoduc Nigéria Maroc (GNM)
16)-Couverture des engagements de la
Société Nationale de Garantie et du
Financement de l’Entreprise (SNGFE) en
matière de financement des bénéficiaires           278,00                  -            278,00        0,52%
de l’opération de relogement des ménages
issus des bidonvilles de la préfecture de
Skhirate-Temara
17)-Financement du programme de mise à
niveau des infrastructures du Football             250,00                  -            250,00        0,47%
national au titre de l’année 2023
18)-Règlement, au profit de la SMIT, de la
1ère tranche prévue par la convention
spécifique pour le déploiement de la feuille           -               225,00           225,00        0,42%
de route stratégique du secteur du
tourisme
19)-Versement au profit de la Société
Moroccan Agency For Sustainable Energy                                     -
                                                    221,88                               221,88       0,42%
(MASEN), au titre de l’augmentation de
son capital social




                                                     Déblocages
                                                                         Déblocages
                                                       effectués                                       Part dans le
                                                                          effectués
                                                   (par imputation                         Total des    total des
                  Opérations                                          (par prélèvement
                                                  sur le budget des                       déblocages   déblocages
                                                                        sur les crédits
                                                       Charges                                           (en %)
                                                                      supplémentaires)
                                                     Communes)
20)-Alimentation en eau potable et en
électricité   du      nouveau    complexe             206,02                  -            206,02        0,39%
industrialo-portuaire Nador West Med
21)-Financement       du    programme       de
réalisation     des      zones     d'activités
économiques dédiées aux unités de                         -               200,00           200,00        0,38%
production     identifiées    à   risque     et
nécessitant une délocalisation au niveau de
la ville de Casablanca et de ses environs
22)-Versement au profit de la SOREAD,
sous forme d’avance en compte courant                 200,00                  -            200,00        0,38%
d’associés
23)-Versement, au profit de la SNRT, de la
subvention exceptionnelle destinée au
financement       de      l'investissement                                    -
                                                      200,00                               200,00        0,38%
nécessaire,  en    termes     de    moyens
techniques, pour la couverture des grands
évènements sportifs
24)-Financement          du         projet
d’interconnexion du barrage Oued El                   200,00                  -            200,00        0,38%
Makhazine avec le barrage Dar Khrofa
25)-Versement au profit de l’agence pour
la  promotion   et    le  développement                                       -
                                                      150,00                               150,00        0,28%
économique et social des Provinces du sud
du Royaume
26)-Règlement de la contribution du
Ministère de l’Economie et des Finances au
financement du programme d’urgence                                                                       ~ noo/
        ....                    ,                      loU,UU                 -            loU,UU        U,zo/o
pour la mise a niveau des zones
frontalières de la Région de l’Oriental au
titre de l’année 2023
27)-Versement au profit de DAMANE
ASSAKANE, au titre du financement des                                         -
                                                      146,00                               146,00        0,28%
produits de garantie « FOGARIM » et
« FOGALOGE »
28)-Versement, au profit de la Société de
Développement        Local      «Marrakech
Mobility», au titre du règlement de la
contribution du Ministère de l’Economie et                                                               nnmz
 .                       £.         .    .            140,00                  -            140,00        0,26%
des     Finances   au    financement    du
programme urgent d’aménagement et de
mise à niveau urbaine de la ville de
Marrakech

29)-Versement au profit de la Régie
Autonome Intercommunale de Distribution
d’Eau et d’Electricité de la Province de Safi
(RADEES), au titre de la contribution du
Ministère de l’Economie et des Finances
pour     l’année     2023,    destinée    au           134,10                 -             134,10       0,25%
financement du projet d’alimentation en
eau potable de la ville de Safi et des zones
rurales concernées des provinces de Safi
et de Youssoufia à partir des stations de
dessalement de l’OCP
| PROJET DE LO! DE FINANCES POUR L’ANNEE 2025 |




                                                  Déblocages
                                                                      Déblocages
                                                    effectués                                       Part dans le
                                                                       effectués
                                                (par imputation                         Total des    total des
                 Opérations                                        (par prélèvement
                                               sur le budget des                       déblocages   déblocages
                                                                     sur les crédits
                                                    Charges                                           (en %)
                                                                   supplémentaires)
                                                  Communes)
30)-Règlement, au profit du CIH, de la
10eme    annuité    de    l’échéancier  des
ristournes d’intérêts à la charge de l’Etat,        132,63                 -            132,63        0,25%
destinée à soutenir la construction et
l’acquisition de logements économiques
31)-Versement au profit de la SMIT,
représentant la contribution de l’Etat au
financement du programme d’appui au                                        -
                                                    90,00                                90,00        0,17%
développement de la TPME touristique
«Programme AL Moukawala Siyahia», au
titre de l’année 2023
32)-Versement au profit de la Fondation                                    -                          0,16%
Nationale des Musées                                85,00                                85,00
33)-Règlement, au profit de l’ANPME, de la
lere tranche prévue par la convention
spécifique pour le déploiement de la feuille           -                58,00            58,00         0,11%
de route stratégique du secteur du
tourisme
34)-Financement du projet intégré dans le
cadre du programme "Marrakech, cité du                 -                45,00            45,00        0,08%
renouveau permanent"
35)-Autres transferts                              1.633,32            1.971,50        3.604,82       6,80%

                    Total                         33.781,17           19.192,92        52.974,09      100%




11.1.2. Crédits alloués et réalisations au titre de la période allant du
1er janvier au 1er juin 2024
Le montant des crédits ouverts au titre du chapitre d’investissement des Charges Communes
pour l’année 2024, s’établit à 43.912 MDH, compte tenu d’une somme de 7.500 MDH
représentant les crédits supplémentaires ouverts par décret et destinés à soutenir certains
établissements et entreprises publics en vue d’améliorer leurs situations financières et
contribuer au financement de leurs projets stratégiques.

En outre, des crédits supplémentaires totalisant 2.500 MDH ont été ouverts, par arrêté du
Ministre des Finances, au cours de de la période allant du 1er janvier au 1er juin 2024,
correspondant aux versements effectués à partir des CAS intitulés « Fonds de remploi
domanial » (2.000 MDH) et « Part des collectivités territoriales dans le produit de la T.V.A »
(500 MDH). Ces crédits ont servi, essentiellement, au financement du CAS : « Fonds national
du développement du sport ».

Au 1er juin 2024, les crédits engagés dans le cadre du chapitre d’investissement des Charges
Communes, ont atteint 17.132,43 MDH, soit un taux d’exécution d’environ 37%.
                                                  NOTE SUR LES DEPENSES RELATIVES AUX CHARGES COMMUNES



Les principaux versements effectués’ à ladite date, au titre dudit chapitre, sont déclinés
comme suit :
                                                         Déblocages
                                                                             Déblocages
                                                           effectués                                       Part dans le
                                                                              effectués
                                                       (par imputation                         Total des    total des
                     Opérations                                           (par prélèvement
                                                      sur le budget des                       déblocages   déblocages
                                                                            sur les crédits
                                                            Charges                                          (en %)
                                                                          supplémentaires)
                                                         Communes)

“□-Versements au             profit   des   comptes
                                                         13.672,77           2.000,00         15.672,77      91,48%
spéciaux du Trésor

2)-Règlement, au profit de l’ONCF, sous                                           -
                                                          500,00                               500,00        2,92%
forme de dotation en capital

3)-Versement au profit de la Société
Nationale    de  Radiodiffusion     et    de                                      -
                                                          327,93                               327,93         1,91%
Télévision (SNRT), au titre de l’acquisition
de MEDI1 TV et MEDI1 Radio

4)-Autres transferts                                       131,73             500,00            631,73       3,69%


                             Total                       14.632,43           2.500,00         17.132,43      100%




11.2. REPARTITION DES CREDITS D’INVESTISSEMENT AU TITRE DE
L’ANNEE 2023 ET DE LA PERIODE ALLANT DU 1er JANVIER AU 1er JUIN
2024

Les crédits d’investissement du budget des Charges Communes peuvent être ventilés en
trois grands postes de dépenses :

     •   Transferts au profit de comptes spéciaux du Trésor ;

     •   Transferts au profit d’établissements et entreprises publics

     •   Autres transferts.


11.2.1. Transferts au profit de comptes spéciaux du Trésor
Le chapitre d’investissement des Charges Communes supporte les transferts au profit des
comptes spéciaux du Trésor destinés, notamment, à la mise en œuvre des stratégies et des
politiques publiques, ainsi qu’à la couverture des dépenses nécessitant l’intervention du
Ministère de l’Economie et des Finances pour la liquidation et la programmation des
montants y afférents sur la base des données prévisionnelles des recettes, ou liés à
l’existence d’engagements à moyen terme pris par ledit ministère.

Le tableau suivant fait ressortir les versements effectués à partir dudit chapitre, au profit de
certains comptes spéciaux du Trésor, au cours de l’année 2023 et de la période allant du
1er janvier au 1er juin 2024 :

*
    En millions de Dirhams
| PROJET DE LO! DE FINANCES POUR L’ANNEE 2025 |




                                                                                                             (En MDH)

                                                                                         2023           2024°

      •       Versements aux comptes d’affectation spéciale, dont :                 21.851,81          5.226,77

          S   Fonds spécial pour la gestion des effets du tremblement de
                                                                                    6.250,00                  -
              terre ayant touché le Royaume du Maroc

          S   Fonds spécial relatif au produit des parts d’impôts affectées
                                                                                        3.255,22        1.477,59
              aux régions
          S   Fonds pour la promotion de l’emploi des jeunes                        2.528,00            177,00

          S   Fonds de soutien à l’initiative nationale pour le développement
                                                                                    2.500,00            750,00
              humain
          S   Fonds National du Développement du Sport                              2.400,00           2.000,00

          S   Part des collectivités territoriales dans le produit de la T.V.A          1.392,00        313,50

          S   Fonds de lutte contre les effets des catastrophes naturelles              1.166,40              -

          S   Fonds d’accompagnement des réformes du transport routier
                                                                                    1.000,00            250,00
              urbain et interurbain
          S   Fonds d'appui au financement de l'entrepreneuriat                         500,00                -

          S   Fonds de solidarité interrégionale                                         361,69             164,18

      •       Versements aux comptes de dépenses sur dotations                      10.884,00          10.446,00

                                         TOTAL                                      32.735,81          15.672,77

              Au 1er juin 2024.


11.2.2. Transferts au profit d’établissements et entreprises publics
Il s’agit d’opérations afférentes à des apports en capital et à des avances en compte courant
d'associés, ainsi que de dépenses liées à la participation du Ministère de l’Economie et des
Finances       au    financement      de    certains     projets    structurants,   à     l’appui,   dans     un     cadre
conventionnel, à la mise en oeuvre de plusieurs stratégies sectorielles, à la restructuration de
certains établissements publics et à l’apurement de leurs dettes.

Les principaux transferts au profit des établissements et entreprises publics, effectués à
partir du chapitre d’investissement des Charges Communes au titre de l’année 2023 et de la
période allant du 1er janvier au 1er juin 2024, sont retracés dans le tableau ci-après :

                                                                                                             (En MDH)

                                                                                         2023           2024°

      •       Office National de l’Electricité et de l’Eau Potable (ONEE)           5.004,89                  -

      •       Office National des Chemins de Fer (ONCF)                                 1.918,04        500,00

      •       Société Marocaine d’ingénierie Touristique (SMIT)                         1.865,00              -

      •       Agence pour l’Aménagement de la Vallée du Bouregreg                       1.564,50            10,00

      •       Compagnie Nationale Royal Air Maroc (RAM)                             1.500,00                  -

      •       Office Régional de Mise en Valeur Agricole de Doukkala                1.000,00                  -

      •       Office National Marocain du Tourisme (ONMT)                               750,00                -
                                              NOTE SUR LES DEPENSES RELATIVES AUX CHARGES COMMUNES




                                                                                   2023            2024°

       •    Société Rabat Région Aménagements                                     604,96           100,00

       •    Crédit Agricole du Maroc                                              500,00              -

       •    Société Nationale de Garantie et du Financement de ('Entreprise       497,00              -
            (SNGFE)

       •    Office National des Hydrocarbures et des Mines (ONHYM)                301,50              -

        •    Société Moroccan Agency For Sustainable Energy (MASEN)               221,88              -

        •    Office Régional de Mise en Valeur Agricole du         Loukkos        200,00              -
             (ORMVAL)
        •    Société d'Etudes et de Réalisations Audiovisuelles (SOREAD)          200,00              -

        •    Société Nationale de Radiodiffusion et de Télévision (SNRT)          200,00           327,93

        •    Société Casablanca Aménagements S.A.                                 200,00              -

        •    Agence pour la Promotion et le Développement Economique              150,00              -
             et Social des Provinces du Sud du Royaume

        •    Régie Autonome Intercommunale de Distribution d’Eau et               134,10              -
             d’Electricité de la Province de Safi (RADEES)
        •    Fondation Nationale des Musées                                       85,00               -

        •    Agence Nationale des Ports (ANP)                                      69,84              -

        •    Agence Nationale pour la Promotion de la Petite et Moyenne           58,00               -
             Entreprise (ANPME)
        •    Fonds Mohammed VI pour l'investissement                              50,00               -

        •    Société Nador West Med                                               50,00               -
        •    Régie Autonome Intercommunale de Distribution d’Eau,
             d’Électricité et de Gestion d’Assainissement Liquide des              32,80              -
             Provinces d’EI Jadida et de Sidi Bennour (RADEEJ)
        •    Société Al Omrane Marrakech                                          26,00               -

                                        TOTAL                                    17.183,51         937,93

     Au 1er juin 2024.



11.2.3. Autres transferts
Les principaux versements effectués à ce titre, portent sur les opérations suivantes :

 •    Règlement          de   la   contribution   du   Ministère   de   l’Economie      et   des   Finances   au
      financement du programme urgent d’aménagement et de mise à niveau urbaine à la
      ville de Marrakech et des travaux complémentaires y afférents (194 MDH en 2023) ;

 •    Ristournes d’intérêts sur les prêts à la construction et autres ristournes (186,48 MDH en
      2023 et 1,74 MDH au 1er juin 2024) ;

 •    Versement          de   la   contribution   du   Ministère   de      l’Economie   et   des   Finances   au
      financement du programme d’urgence pour la mise à niveau des zones frontalières de
      la région de l’Oriental (150 MDH en 2023).
| PROJET DE LO! DE FINANCES POUR L’ANNEE 2025 |




CHAPITRE III - PRESENTATION DU PROJET DE
BUDGET DES CHARGES COMMUNES AU TITRE DE
L'ANNEE 2025

Il 1.1. VOLUME GLOBAL

Les crédits prévus par le projet de loi de finances pour l’année 2025 au titre des chapitres de
fonctionnement   et d’investissement du budget         des   Charges   Communes,     s’élèvent,
respectivement, à 48.112 MDH et 43.602 MDH.


III.2. CREDITS DE FONCTIONNEMENT

Le montant des crédits programmés au chapitre de fonctionnement des Charges Communes
pour l’année 2025, affiche une hausse de 13.292 MDH ou +38,17% par rapport aux crédits
ouverts par la loi de finances pour l’année 2024.

Les principales rubriques dudit chapitre sont constituées par les transferts au titre des
opérations suivantes :

► Contribution au financement du chantier de généralisation de la protection sociale :
      16.289 MDH ;

► Soutien des prix et mesures d’accompagnement : 17.136 MDH

Ce montant est ventilé comme suit :

  •     Couverture de la charge de compensation du gaz butane et de certaines denrées
       alimentaires de base : 16.536 MDH ;

  •     Prise en charge de l’impact des mesures d’accompagnement à travers le soutien du
       secteur du transport : 600 MDH.

► Couverture du déficit du régime des pensions militaires, des allocations familiales des
      retraités, des dépenses des régimes non cotisants, ainsi que d’autres dépenses liées
      aux régimes de retraite gérés par la CMR : 5.211,69 MDH ;

► Versements à d’autres comptes spéciaux du Trésor : 980 MDH

► Dépenses diverses et exceptionnelles (couverture d’autres dépenses à caractère
      social) : 8.495,31 MDH


111.3. CREDITS D’INVESTISSEMENT

Le montant des crédits prévus au titre du chapitre d’investissement des Charges Communes
pour l’année 2025, s’élève à 43.602 MDH, en hausse de 7.190 MDH ou de +19,75% par rapport
à l’année 2024.
                                           NOTE SUR LES DEPENSES RELATIVES AUX CHARGES COMMUNES



Les principales composantes du chapitre d’investissement des Charges Communes sont les
suivantes :

► Versements au profit des comptes spéciaux du Trésor : 24.172,9 MDH

  •   Comptes d’affectation spéciale : 13.247,9 MDH, dont :

      J      Fonds d’appui à la protection sociale et à la cohésion sociale : 4.250 MDH ;

      J      Fonds spécial    relatif au   produit des parts d’impôts affectées aux régions :
             1.893,96 MDH et Fonds de solidarité interrégionale : 210,44 MDH ;

      J      Fonds pour la promotion de l’emploi des jeunes : 2.000 MDH ;

      J      Fonds de soutien à l’initiative nationale pour le développement humain : 1.500 MDH;

      J      Part des collectivités territoriales dans le produit de la T.V.A : 1.203,50 MDH ;

      J      Fonds d’accompagnement des réformes du transport routier urbain et interurbain :
             1.000 MDH ;

      J      Fonds de lutte contre les effets des catastrophes naturelles : 745 MDH.

  •   Comptes de dépenses sur dotations : 10.925 MDH.

► Participations et concours divers : 19.237,1 MDH ;

Cette rubrique comprend, essentiellement, les transferts pour le financement des opérations
ci-après :

  •   Dotations en capital au profit de certains EEP : 2.287 MDH ;

  •   Accompagnement de la construction de stations de dessalement et transferts d’eau
      1.660 MDH ;

  •   Versement au profit de la Société Nationale de Garantie et du Financement de
      ('Entreprise (SNGFE) : 1.281 MDH ;

  •   Développement du partenariat public-privé (PPP) pour les projets d'irrigation et
      d'aménagement de l’espace agricole : 1.000 MDH ;

  •   Programme de recasement des bidonvilles de Casa-Settat : 1.000 MDH ;

  •   Versement à la Fondation Mohamed VI des Science et de la Santé : 924 MDH ;

  •   Versements au profit des agences pour la promotion et le développement économique
      et social des provinces du Nord, du Sud et de l’Oriental : 500 MDH ;

  •   Versement dans le cadre de certaines conventions relatives au programme d'urgence
      de l'eau : 418,60 MDH ;

  •   Subvention à l'ONMT : 400 MDH ;

  •   Subvention à l'OFPPT au titre du programme relatif aux Cités des Métiers et des
      Compétences (CMC) : 400 MDH ;
PROJET DE LOI DE FINANCES POUR L’ANNEE 2025 |




 •   Prise   en   charge   par   l’Etat   du    crédit   TVA   détenu   par   l’ONEE (360,08   MDH),
     l’ONCF (301,77 MDH) et l’ADM (368,27 MDH) ;

 •   Remboursement de la différence entre le coût et le prix de l’eau dessalée de la station
     de dessalement de la province de Chtouka Ait Baha : 324 MDH.

           
"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("PLF2025: Explorez le rapport sur les dépenses relatives aux charges communes à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

        # Afficher toujours la barre de saisie
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
    selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
    query_input = st.text_input("", key="text_input_query", placeholder="Posez votre question ici...", help="Posez votre question ici...")
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

    if query_input and query_input not in st.session_state.previous_question:
        query = query_input
        st.session_state.previous_question.append(query_input)
    elif selected_questions:
        query = selected_questions
    else:
        query = ""

    if query :
        st.session_state.conversation_history.add_user_message(query) 
        if "Donnez-moi un résumé du rapport" in query:
            summary="""Le document est une note explicative du Projet de Loi de Finances (PLF) pour l’année 2025, se concentrant sur les dépenses relatives aux charges communes. Il présente les grandes orientations budgétaires, les priorités de financement et la répartition des dépenses pour couvrir les besoins communs de l’État. Ce projet vise à optimiser l’utilisation des ressources publiques, en soutenant des initiatives prioritaires dans divers secteurs, comme l’éducation, la santé, et le développement social. Le document souligne également les efforts pour renforcer la transparence et l’efficacité budgétaire afin de répondre aux enjeux socio-économiques du pays pour l’année à venir."""
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte donnee des réponse significatif et bien formé essayer de ne pas dire que information nest pas mentionné dans le texte si tu ne trouve pas essayer de repondre dapres votre connaissance ms focaliser sur ce texte en premier: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

            summary = response['choices'][0]['message']['content']
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary)  # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
            # Format et afficher les messages comme précédemment
        formatted_messages = []
        previous_role = None 
        if st.session_state.conversation_history.messages: # Variable pour stocker le rôle du message précédent
                for msg in conversation_history.messages:
                    role = "user" if msg.type == "human" else "assistant"
                    avatar = "🧑" if role == "user" else "🤖"
                    css_class = "user-message" if role == "user" else "assistant-message"

                    if role == "user" and previous_role == "assistant":
                        message_div = f'<div class="{css_class}" style="margin-top: 25px;">{msg.content}</div>'
                    else:
                        message_div = f'<div class="{css_class}">{msg.content}</div>'

                    avatar_div = f'<div class="avatar">{avatar}</div>'
                
                    if role == "user":
                        formatted_message = f'<div class="message-container user"><div class="message-avatar">{avatar_div}</div><div class="message-content">{message_div}</div></div>'
                    else:
                        formatted_message = f'<div class="message-container assistant"><div class="message-content">{message_div}</div><div class="message-avatar">{avatar_div}</div></div>'
                
                    formatted_messages.append(formatted_message)
                    previous_role = role  # Mettre à jour le rôle du message précédent

                messages_html = "\n".join(formatted_messages)
                st.markdown(messages_html, unsafe_allow_html=True)
if __name__ == '__main__':
    main()
