''' 
Report functie

Het moet natuurlijk aanvoelen, report begint met report, dan product (dat ook total mag zijn of een lijst producten), 
dan eventueel welke dag, current date als standaard, (mogelijk ook periode als week x of start datum - eind datum) of totaal.
Dan een keuze, blanco (dus alleen bovenstaande), profit, bought, sold, expired, stock waarvan er één mag.
Tenslotte nog -graph of -chart of -weetiknogniet voor als je het mooi in beeld hebben wil.
Gaat  eruitzien als: report banana 2023-05-30 stock -chart.
 

Dag(default=today)
    Alles wat er die dag gebeurd is, gekocht, verkocht, expired
    functie today_activity returned de volgende lijst: [[buy][sell][expired]]
    de report functie haalt de info eruit

-product(default=all)
    Optioneel: Hoeveel van alleen dit product gekocht, verkocht of expired is
    today_activity een product argument geven

-profit
    Optioneel: Het bedrag dat verdiend is per product
    Een calc_profit functie maken, of calc_stock ook profit laten doen

-stock
    Optioneel: Wat de huidige stock is, totaal of het aangegeven product
    calc_stock een totaalfunctie geven

-grafiek
    Optioneel: Moet ik nog uitwerken





De calc_profit functie krijgt als argumenten: 
Product
alle ipv product
Datum=vandaag
totaal ipv datum 

de functie moet terugsturen:
    Alles op aangegeven dag en aangegeven product ofc

    expired product en hoeveel geld het verneukte
        filter nog houdbare producten eruit
        van elke buy code die verlopen is een .sum() uit laten voeren
        is er een .sum() > 0? Dan is het verlopen op expiracy date
    
    Hoeveel verkocht van product en hoeveel het opleverde

    Hoeveel van een product nog in omloop is(?)
    

    De functie die de namespace handelt regelt ook de eventuele grafiek, dat doet deze niet
    '''
