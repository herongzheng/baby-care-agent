CREATE TABLE daily_event.pee_records (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pee_time datetime,
  amount VARCHAR(128),
  is_normal bool default true
);

INSERT INTO daily_event.pee_records(pee_time, amount)
values("2025-11-22 10:28:08", "large");

INSERT INTO daily_event.pee_records(pee_time, amount)
values("2025-11-22 03:25:15", "super");

INSERT INTO daily_event.pee_records(pee_time, amount)
values("2025-11-22 06:15:32", "small");