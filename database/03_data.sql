INSERT INTO roles (nombre, descripcion) VALUES ('ADMINISTRADOR', 'Gestiona usuarios, configuración y todos los módulos');
INSERT INTO roles (nombre, descripcion) VALUES ('SUPERVISOR', 'Supervisa SLA, tickets, órdenes y reportes');
INSERT INTO roles (nombre, descripcion) VALUES ('TECNICO', 'Atiende tickets y órdenes asignadas');
INSERT INTO roles (nombre, descripcion) VALUES ('CLIENTE', 'Crea y consulta sus solicitudes');

INSERT INTO sla (nombre, prioridad, horas_respuesta, horas_resolucion) VALUES ('Crítico 24x7', 'P1', 0.25, 2);
INSERT INTO sla (nombre, prioridad, horas_respuesta, horas_resolucion) VALUES ('Alta 24x7', 'P2', 0.5, 4);
INSERT INTO sla (nombre, prioridad, horas_respuesta, horas_resolucion) VALUES ('Estándar', 'P3', 1, 8);

INSERT INTO clientes (razon_social, identificacion_fiscal, correo_contacto, estado)
VALUES ('Banco Santander', '20100047213', 'soporte@bancosantander.example', 'ACTIVO');
INSERT INTO clientes (razon_social, identificacion_fiscal, correo_contacto, estado)
VALUES ('Clínica San Patricio', '20492819001', 'ti@clinicasanpatricio.example', 'AUDITORIA');

COMMIT;
