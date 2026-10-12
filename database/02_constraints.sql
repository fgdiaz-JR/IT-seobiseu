ALTER TABLE roles ADD CONSTRAINT uq_roles_nombre UNIQUE (nombre);
ALTER TABLE usuarios ADD CONSTRAINT uq_usuarios_correo UNIQUE (correo);
ALTER TABLE usuarios ADD CONSTRAINT fk_usuarios_rol FOREIGN KEY (rol_id) REFERENCES roles(id);
ALTER TABLE usuarios ADD CONSTRAINT ck_usuarios_activo CHECK (activo IN ('S', 'N'));

ALTER TABLE clientes ADD CONSTRAINT uq_clientes_identificacion UNIQUE (identificacion_fiscal);
ALTER TABLE clientes ADD CONSTRAINT ck_clientes_estado CHECK (estado IN ('ACTIVO', 'AUDITORIA', 'RENOVACION', 'INACTIVO'));
ALTER TABLE sedes ADD CONSTRAINT fk_sedes_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id);
ALTER TABLE sla ADD CONSTRAINT ck_sla_prioridad CHECK (prioridad IN ('P1', 'P2', 'P3'));
ALTER TABLE sla ADD CONSTRAINT ck_sla_horas CHECK (horas_respuesta > 0 AND horas_resolucion > 0);

ALTER TABLE tickets ADD CONSTRAINT fk_tickets_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id);
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_sede FOREIGN KEY (sede_id) REFERENCES sedes(id);
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_creador FOREIGN KEY (creado_por) REFERENCES usuarios(id);
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_asignado FOREIGN KEY (asignado_a) REFERENCES usuarios(id);
ALTER TABLE tickets ADD CONSTRAINT fk_tickets_sla FOREIGN KEY (sla_id) REFERENCES sla(id);
ALTER TABLE tickets ADD CONSTRAINT ck_tickets_prioridad CHECK (prioridad IN ('P1', 'P2', 'P3'));
ALTER TABLE tickets ADD CONSTRAINT ck_tickets_estado CHECK (estado IN ('ABIERTO', 'EN_PROCESO', 'ESPERA', 'RESUELTO', 'CERRADO'));

ALTER TABLE ordenes_trabajo ADD CONSTRAINT fk_ordenes_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(id);
ALTER TABLE ordenes_trabajo ADD CONSTRAINT fk_ordenes_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id);
ALTER TABLE ordenes_trabajo ADD CONSTRAINT fk_ordenes_tecnico FOREIGN KEY (tecnico_id) REFERENCES usuarios(id);
ALTER TABLE ordenes_trabajo ADD CONSTRAINT ck_ordenes_prioridad CHECK (prioridad IN ('P1', 'P2', 'P3'));
ALTER TABLE ordenes_trabajo ADD CONSTRAINT ck_ordenes_estado CHECK (estado IN ('PENDIENTE', 'EN_PROCESO', 'DIAGNOSTICO', 'COMPLETADA', 'CANCELADA'));

ALTER TABLE inventario ADD CONSTRAINT uq_inventario_sku UNIQUE (sku);
ALTER TABLE inventario ADD CONSTRAINT ck_inventario_stock CHECK (stock >= 0 AND stock_minimo >= 0);
ALTER TABLE inventario ADD CONSTRAINT ck_inventario_precio CHECK (precio_unitario >= 0);
ALTER TABLE movimientos_inventario ADD CONSTRAINT fk_movimientos_inventario FOREIGN KEY (inventario_id) REFERENCES inventario(id);
ALTER TABLE movimientos_inventario ADD CONSTRAINT fk_movimientos_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
ALTER TABLE movimientos_inventario ADD CONSTRAINT ck_movimientos_tipo CHECK (tipo IN ('ENTRADA', 'SALIDA', 'AJUSTE'));
ALTER TABLE movimientos_inventario ADD CONSTRAINT ck_movimientos_cantidad CHECK (cantidad > 0);

ALTER TABLE bitacora_tickets ADD CONSTRAINT fk_bitacora_ticket FOREIGN KEY (ticket_id) REFERENCES tickets(id);
ALTER TABLE bitacora_tickets ADD CONSTRAINT fk_bitacora_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
