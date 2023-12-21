
CREATE(Portugal:Country {name:"Portugal"})
CREATE(Braga:Cities {name:"Braga"})
CREATE (Barcelos:Cities {name:"Barcelos"})
CREATE(Euro:Currency {name:"Euro", symbol:"€"})
CREATE 
(Barcelos)-[:CITY_IN]->(Braga),
(Braga)-[:CITY_IN]->(Braga),
(Braga)-[:DISTRICT_IN]->(Portugal),
(Barcelos)-[:CITY_IN]->(Portugal),
(Euro)-[:USED_IN]->(Portugal)

CREATE(Addr1:Address {name:"Addr1", rua:"rua 1", nr:"1"})
CREATE(Addr2:Address {name:"Addr2", rua:"rua 2", nr:"2"})
CREATE(Addr3:Address {name:"Addr3", rua:"rua 3", nr:"3"})

CREATE
(Addr1)-[:ADDR_IN]->(Barcelos),
(Addr2)-[:ADDR_IN]->(Barcelos),
(Addr3)-[:ADDR_IN]->(Braga)

CREATE(User1:User {name:"User 1", email:"user1@user1.com", username:"user1", password:"pass", enabled:true})
CREATE(User2:User {name:"User 2", email:"user2@user2.com", username:"user2", password:"pass", enabled:true})
CREATE(User3:User {name:"User 3", email:"user3@user3.com", username:"user3", password:"pass", enabled:true})
CREATE(User4:User {name:"User 4", email:"user4@user4.com", username:"user4", password:"pass", enabled:true})

CREATE(Administrador:Role {name:"admin"})
CREATE(Utilizador:Role {name:"user"})
CREATE(Convidado:Role {name:"convidado"})

CREATE
(User1)-[:ROLE_IN]->(Administrador),
(User2)-[:ROLE_IN]->(Utilizador),
(User3)-[:ROLE_IN]->(Utilizador),
(User4)-[:ROLE_IN]->(Convidado)

CREATE(Park1:Parkings {name:"park1",latitude:1, longitude:1, enabled:true})
CREATE(Park2:Parkings {name:"park2",latitude:2, longitude:2, enabled:true})
CREATE(Park3:Parkings {name:"park3",latitude:3, longitude:3, enabled:true})

CREATE
(Park1)-[:LOCATED_IN]->(Addr1),
(Park2)-[:LOCATED_IN]->(Addr2),
(Park3)-[:LOCATED_IN]->(Addr3)

CREATE(Park1_occupation:Occupation {name:"park1_o",percentage: 10, last_updated_min:1})
CREATE(Park2_occupation:Occupation {name:"park2_o",percentage: 20, last_updated_min:2})
CREATE(Park3_occupation:Occupation {name:"park3_o",percentage: 30, last_updated_min:3})

CREATE
(Park1)-[:OCCUPATION_IN]->(Park1_occupation),
(Park2)-[:OCCUPATION_IN]->(Park2_occupation),
(Park3)-[:OCCUPATION_IN]->(Park3_occupation)


CREATE(Order1_0:Order {name:"Order1_0",time:timestamp(), arrival:datetime("2023-01-01T18:40:00")})
CREATE(Order1_1:Order {name:"Order1_1",time:timestamp(), arrival:datetime("2023-01-01T19:40:00")})
CREATE(Order1_2:Order {name:"Order1_2",time:timestamp(), arrival:datetime("2023-01-01T20:40:00")})
CREATE(Order2_0:Order {name:"Order2_0",time:timestamp(), arrival:datetime("2023-02-01T18:40:00")})
CREATE(Order2_1:Order {name:"Order2_1",time:timestamp(), arrival:datetime("2023-02-01T19:40:00")})
CREATE(Order2_2:Order {name:"Order2_2",time:timestamp(), arrival:datetime("2023-02-01T20:40:00")})
CREATE(Order3_0:Order {name:"Order3_0",time:timestamp(), arrival:datetime("2023-03-01T18:40:00")})
CREATE(Order3_1:Order {name:"Order3_1",time:timestamp(), arrival:datetime("2023-03-01T19:40:00")})
CREATE(Order3_2:Order {name:"Order3_2",time:timestamp(), arrival:datetime("2023-03-01T20:40:00")})

CREATE
(Order1_0)-[:SEARCH_IN]->(Addr1),
(Order1_1)-[:SEARCH_IN]->(Addr2),
(Order1_2)-[:SEARCH_IN]->(Addr1),
(Order2_0)-[:SEARCH_IN]->(Addr2),
(Order2_1)-[:SEARCH_IN]->(Addr3),
(Order2_2)-[:SEARCH_IN]->(Addr1),
(Order3_0)-[:SEARCH_IN]->(Addr3),
(Order3_1)-[:SEARCH_IN]->(Addr1),
(Order3_2)-[:SEARCH_IN]->(Addr2)

CREATE
(User1)-[:RESERVE_IN]->(Order1_0),
(User1)-[:RESERVE_IN]->(Order1_1),
(User1)-[:RESERVE_IN]->(Order1_2),
(User2)-[:RESERVE_IN]->(Order2_0),
(User2)-[:RESERVE_IN]->(Order2_1),
(User2)-[:RESERVE_IN]->(Order2_2),
(User3)-[:RESERVE_IN]->(Order3_0),
(User3)-[:RESERVE_IN]->(Order3_1),
(User3)-[:RESERVE_IN]->(Order3_2)

CREATE
(Order1_0)-[:RESERVE_IN]->(Park1),
(Order1_1)-[:RESERVE_IN]->(Park2),
(Order1_2)-[:RESERVE_IN]->(Park3),
(Order2_0)-[:RESERVE_IN]->(Park2),
(Order2_1)-[:RESERVE_IN]->(Park1),
(Order2_2)-[:RESERVE_IN]->(Park3),
(Order3_0)-[:RESERVE_IN]->(Park3),
(Order3_1)-[:RESERVE_IN]->(Park2),
(Order3_2)-[:RESERVE_IN]->(Park3)

CREATE
(Order1_0)-[:PREVIOUS_IN]->(Order1_1),
(Order1_1)-[:PREVIOUS_IN]->(Order1_2),
(Order2_0)-[:PREVIOUS_IN]->(Order2_1),
(Order2_1)-[:PREVIOUS_IN]->(Order2_2),
(Order3_0)-[:PREVIOUS_IN]->(Order3_1),
(Order3_1)-[:PREVIOUS_IN]->(Order3_2)

CREATE(Response1_0:Response {name:"Response1_0", time:timestamp(), response:true})
CREATE(Response1_1:Response {name:"Response1_1", time:timestamp(), response:true})
CREATE(Response1_2:Response {name:"Response1_2", time:timestamp(), response:true})
CREATE(Response2_0:Response {name:"Response2_0", time:timestamp(), response:true})
CREATE(Response2_1:Response {name:"Response2_1", time:timestamp(), response:true})
CREATE(Response2_2:Response {name:"Response2_2", time:timestamp(), response:true})
CREATE(Response3_0:Response {name:"Response3_0", time:timestamp(), response:true})
CREATE(Response3_1:Response {name:"Response3_1", time:timestamp(), response:true})
CREATE(Response3_2:Response {name:"Response3_2", time:timestamp(), response:true})

CREATE
(Response1_0)-[:RESPONSE_IN]->(Order1_0),
(Response1_1)-[:RESPONSE_IN]->(Order1_1),
(Response1_2)-[:RESPONSE_IN]->(Order1_2),
(Response2_0)-[:RESPONSE_IN]->(Order2_0),
(Response2_1)-[:RESPONSE_IN]->(Order2_1),
(Response2_2)-[:RESPONSE_IN]->(Order2_2),
(Response3_0)-[:RESPONSE_IN]->(Order3_0),
(Response3_1)-[:RESPONSE_IN]->(Order3_1),
(Response3_2)-[:RESPONSE_IN]->(Order3_2)


Create(Review1_0:Review {name:"Review1_0", positiva: true, descricao: "ok"})
Create(Review1_1:Review {name:"Review1_1", positiva: true, descricao: "ok"})
Create(Review1_2:Review {name:"Review1_2", positiva: true, descricao: "ok"})
Create(Review2_0:Review {name:"Review2_0", positiva: true, descricao: "ok"})
Create(Review2_1:Review {name:"Review2_1", positiva: true, descricao: "ok"})
Create(Review2_2:Review {name:"Review2_2", positiva: false, descricao: "problema"})
Create(Review3_0:Review {name:"Review3_0", positiva: true, descricao: "ok"})
Create(Review3_1:Review {name:"Review3_1", positiva: true, descricao: "ok"})
Create(Review3_2:Review {name:"Review3_2", positiva: true, descricao: "ok"})

CREATE
(Review1_0)-[:REVIEW_IN]->(Order1_0),
(Review1_1)-[:REVIEW_IN]->(Order1_1),
(Review1_2)-[:REVIEW_IN]->(Order1_2),
(Review2_0)-[:REVIEW_IN]->(Order2_0),
(Review2_1)-[:REVIEW_IN]->(Order2_1),
(Review2_2)-[:REVIEW_IN]->(Order2_2),
(Review3_0)-[:REVIEW_IN]->(Order3_0),
(Review3_1)-[:REVIEW_IN]->(Order3_1),
(Review3_2)-[:REVIEW_IN]->(Order3_2)
