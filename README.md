Generate tradecard
===================

This project aims at generating trade cards based on a dedicated CSV file.

The CSV file contains the metadata for the card (period_table_fr_metadata.csv).

The card background is the same for all the cards (assets/background.png).

The card rendering process is performed in the following way :
1. load the atom image and draw it
2. load the card background and draw it on top
3. write the atom metadata on the image
4. draw the atom group on top of the image
