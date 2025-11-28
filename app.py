import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from repository import (
    create_satellite, get_all_satellites, update_satellite, delete_satellite,
    create_zone, get_all_zones, update_zone, delete_zone,
    create_assignment, get_all_assignments, update_assignment, delete_assignment,
    create_log, get_logs
)
from db_connection import test_connection

class SACISApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SACIS - Sistema de Coordinación Satelitals")
        self.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self)
        self.tab_sat = ttk.Frame(tab_control)
        self.tab_zone = ttk.Frame(tab_control)
        self.tab_assign = ttk.Frame(tab_control)
        self.tab_log = ttk.Frame(tab_control)

        tab_control.add(self.tab_sat, text='Satélites')
        tab_control.add(self.tab_zone, text='Zonas')
        tab_control.add(self.tab_assign, text='Asignaciones')
        tab_control.add(self.tab_log, text='Logs')
        tab_control.pack(expand=1, fill='both')

        self.build_sat_tab()
        self.build_zone_tab()
        self.build_assign_tab()
        self.build_log_tab()

    # ---------- SATELLITES TAB ----------
    def build_sat_tab(self):
        frame = self.tab_sat
        left = ttk.Frame(frame, width=300)
        left.pack(side='left', fill='y', padx=8, pady=8)
        right = ttk.Frame(frame)
        right.pack(side='right', expand=True, fill='both', padx=8, pady=8)

        # List
        self.sat_list = tk.Listbox(left, height=25)
        self.sat_list.pack(fill='y', expand=True)
        self.sat_list.bind("<<ListboxSelect>>", self.on_sat_select)

        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text="Nuevo", command=self.new_sat).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Editar", command=self.edit_sat).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_sat).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Actualizar", command=self.refresh_sats).pack(side='left', fill='x', expand=True)

        # Details
        self.sat_details = tk.Text(right, state='disabled')
        self.sat_details.pack(expand=True, fill='both')
        self.refresh_sats()

    def refresh_sats(self):
        self.sat_list.delete(0, tk.END)
        self.sat_items = get_all_satellites()
        for s in self.sat_items:
            avail = '' if s.available else ''
            self.sat_list.insert(tk.END, f"{s.id} - {s.name} [{s.status}] {avail}")

    def on_sat_select(self, event):
        sel = self.sat_list.curselection()
        if not sel:
            return
        idx = sel[0]
        s = self.sat_items[idx]
        txt = f"ID: {s.id}\nNombre: {s.name}\nEstado: {s.status}\nDisponible: {s.available}"
        self.sat_details.configure(state='normal')
        self.sat_details.delete('1.0', tk.END)
        self.sat_details.insert(tk.END, txt)
        self.sat_details.configure(state='disabled')

    def new_sat(self):
        name = simpledialog.askstring("Nuevo satélite", "Nombre:")
        if not name:
            return
        create_satellite(name=name)
        create_log("satellite_create", f"Creado satélite: {name}")
        self.refresh_sats()

    def edit_sat(self):
        sel = self.sat_list.curselection()
        if not sel:
            messagebox.showinfo("Editar", "Selecciona un satélite.")
            return
        s = self.sat_items[sel[0]]
        new_name = simpledialog.askstring("Editar satélite", "Nombre:", initialvalue=s.name)
        if new_name:
            update_satellite(s.id, name=new_name)
            create_log("satellite_update", f"Satélite {s.id} renombrado a {new_name}")
            self.refresh_sats()

    def delete_sat(self):
        sel = self.sat_list.curselection()
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona un satélite.")
            return
        s = self.sat_items[sel[0]]
        if messagebox.askyesno("Confirmar", f"Eliminar satélite {s.id} - {s.name}?"):
            delete_satellite(s.id)
            create_log("satellite_delete", f"Satélite {s.id} eliminado")
            self.refresh_sats()

    # ---------- ZONES TAB ----------
    def build_zone_tab(self):
        frame = self.tab_zone
        left = ttk.Frame(frame, width=300)
        left.pack(side='left', fill='y', padx=8, pady=8)
        right = ttk.Frame(frame)
        right.pack(side='right', expand=True, fill='both', padx=8, pady=8)

        self.zone_list = tk.Listbox(left, height=25)
        self.zone_list.pack(fill='y', expand=True)
        self.zone_list.bind("<<ListboxSelect>>", self.on_zone_select)

        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill='x')
        ttk.Button(btn_frame, text="Nuevo", command=self.new_zone).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Editar", command=self.edit_zone).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_zone).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Actualizar", command=self.refresh_zones).pack(side='left', fill='x', expand=True)

        self.zone_details = tk.Text(right, state='disabled')
        self.zone_details.pack(expand=True, fill='both')
        self.refresh_zones()

    def refresh_zones(self):
        self.zone_list.delete(0, tk.END)
        self.zone_items = get_all_zones()
        for z in self.zone_items:
            restr = '🔒' if z.restricted else ''
            self.zone_list.insert(tk.END, f"{z.id} - {z.name} [{z.priority}] {restr}")

    def on_zone_select(self, event):
        sel = self.zone_list.curselection()
        if not sel:
            return
        z = self.zone_items[sel[0]]
        txt = f"ID: {z.id}\nNombre: {z.name}\nPrioridad: {z.priority}"
        self.zone_details.configure(state='normal')
        self.zone_details.delete('1.0', tk.END)
        self.zone_details.insert(tk.END, txt)
        self.zone_details.configure(state='disabled')

    def new_zone(self):
        name = simpledialog.askstring("Nueva zona", "Nombre de zona:")
        if not name:
            return
        priority = simpledialog.askstring("Prioridad", "Prioridad (CRITICO/ALTO/MEDIO/BAJO):", initialvalue="MEDIO")
        create_zone(name=name, priority=priority if priority else "MEDIO")
        create_log("zone_create", f"Creada zona: {name}")
        self.refresh_zones()

    def edit_zone(self):
        sel = self.zone_list.curselection()
        if not sel:
            messagebox.showinfo("Editar", "Selecciona una zona.")
            return
        z = self.zone_items[sel[0]]
        new_name = simpledialog.askstring("Editar zona", "Nombre:", initialvalue=z.name)
        if new_name:
            update_zone(z.id, name=new_name)
            create_log("zone_update", f"Zona {z.id} renombrada a {new_name}")
            self.refresh_zones()

    def delete_zone(self):
        sel = self.zone_list.curselection()
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona una zona.")
            return
        z = self.zone_items[sel[0]]
        if messagebox.askyesno("Confirmar", f"Eliminar zona {z.id} - {z.name}?"):
            delete_zone(z.id)
            create_log("zone_delete", f"Zona {z.id} eliminada")
            self.refresh_zones()

    # ---------- ASSIGNMENTS TAB ----------
    def build_assign_tab(self):
        frame = self.tab_assign
        top = ttk.Frame(frame)
        top.pack(side='top', fill='x', padx=8, pady=8)
        ttk.Button(top, text="Nueva Asignación", command=self.new_assignment).pack(side='left')
        ttk.Button(top, text="Actualizar lista", command=self.refresh_assigns).pack(side='left')

        self.assign_tree = ttk.Treeview(frame, columns=('id','sat','zone','freq','status'), show='headings')
        self.assign_tree.heading('id', text='ID')
        self.assign_tree.heading('sat', text='Satélite')
        self.assign_tree.heading('zone', text='Zona')
        self.assign_tree.heading('freq', text='Freq (min)')
        self.assign_tree.heading('status', text='Estado')
        self.assign_tree.pack(expand=True, fill='both', padx=8, pady=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', padx=8, pady=8)
        ttk.Button(btn_frame, text="Marcar en curso", command=lambda: self.change_assign_status('en_curso')).pack(side='left')
        ttk.Button(btn_frame, text="Marcar completada", command=lambda: self.change_assign_status('completada')).pack(side='left')
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_assignment_ui).pack(side='left')

        self.refresh_assigns()

    def refresh_assigns(self):
        for i in self.assign_tree.get_children():
            self.assign_tree.delete(i)
        self.assign_items = get_all_assignments()
        sats = {s.id: s for s in getattr(self, 'sat_items', [])}
        zones = {z.id: z for z in getattr(self, 'zone_items', [])}
        # Ensure satellites and zones are refreshed too
        self.refresh_sats()
        self.refresh_zones()
        sats = {s.id: s for s in self.sat_items}
        zones = {z.id: z for z in self.zone_items}
        for a in self.assign_items:
            sat_name = sats.get(a.satellite_id).name if sats.get(a.satellite_id) else str(a.satellite_id)
            zone_name = zones.get(a.zone_id).name if zones.get(a.zone_id) else str(a.zone_id)
            self.assign_tree.insert('', tk.END, values=(a.id, sat_name, zone_name, a.frequency_minutes, a.status))

    def new_assignment(self):
     
        sats = get_all_satellites()
        zones = get_all_zones()
        if not sats or not zones:
            messagebox.showinfo("Asignación", "Necesitas al menos un satélite y una zona.")
            return
        sat_choices = {str(s.id): s for s in sats}
        zone_choices = {str(z.id): z for z in zones}
        sat_id = simpledialog.askstring("Asignar", f"ID Satélite (opciones: {', '.join(sat_choices.keys())}):")
        zone_id = simpledialog.askstring("Asignar", f"ID Zona (opciones: {', '.join(zone_choices.keys())}):")
        freq = simpledialog.askinteger("Frecuencia", "Frecuencia en minutos:", initialvalue=60)
        if sat_id and zone_id:
            try:
                new_id = create_assignment(int(sat_id), int(zone_id), frequency_minutes=(freq or 60))
                create_log("assignment_create", f"Asignación {new_id} sat:{sat_id} zona:{zone_id}")
                messagebox.showinfo("OK", f"Asignación creada. ID {new_id}")
                self.refresh_assigns()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def change_assign_status(self, new_status):
        sel = self.assign_tree.selection()
        if not sel:
            messagebox.showinfo("Estado", "Selecciona una asignación.")
            return
        item = self.assign_tree.item(sel[0])
        aid = item['values'][0]
        update_assignment(aid, status=new_status)
        create_log("assignment_update", f"Asignación {aid} -> {new_status}")
        self.refresh_assigns()

    def delete_assignment_ui(self):
        sel = self.assign_tree.selection()
        if not sel:
            messagebox.showinfo("Eliminar", "Selecciona una asignación.")
            return
        item = self.assign_tree.item(sel[0])
        aid = item['values'][0]
        if messagebox.askyesno("Confirmar", f"Eliminar asignación {aid}?"):
            delete_assignment(aid)
            create_log("assignment_delete", f"Asignación {aid} eliminada")
            self.refresh_assigns()

    # ---------- LOGS TAB ----------
    def build_log_tab(self):
        frame = self.tab_log
        top = ttk.Frame(frame)
        top.pack(side='top', fill='x')
        ttk.Button(top, text="Refrescar logs", command=self.refresh_logs).pack(side='left')
        ttk.Button(top, text="Probar conexión DB", command=self.check_conn).pack(side='left')

        self.log_text = tk.Text(frame, state='disabled')
        self.log_text.pack(expand=True, fill='both', padx=8, pady=8)
        self.refresh_logs()

    def refresh_logs(self):
        logs = get_logs(200)
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        for l in logs:
            ts = l['created_at'].strftime("%Y-%m-%d %H:%M:%S") if l.get('created_at') else ''
            self.log_text.insert(tk.END, f"[{ts}] {l.get('event_type')} - {l.get('details')}\n")
        self.log_text.configure(state='disabled')

    def check_conn(self):
        try:
            test_connection()
            messagebox.showinfo("DB", "ConexionOK (ver consola).")
        except Exception as e:
            messagebox.showerror("DB", f"Error: {e}")

if __name__ == '__main__':
    app = SACISApp()
    app.mainloop()