
function formTRDData() {
    return {
        formularioAbierto: false,
        mostrarModalNuevaVersion: false,
        catalogo: {"series":[]},
        oficinaProductora: "JURIDICA",
        serieSeleccionadaIdx: '',
        
        serieCodigo: '',
        serieNombre: '',
        serie_soporte_papel: false,
        serie_soporte_electronico: false,
        serie_extensiones: '',
        serie_retencion_gestion: '',
        serie_retencion_central: '',
        serie_disposicion_final: '',
        serie_reproduccion_tecnica: '',
        
        tieneSubserie: false,
        subseries: [],
        
        // SubForm para entrada fija y ágil de subseries (bajar a la lista)
        subForm_editandoIdx: null,
        subForm_codigo: '',
        subForm_nombre: '',
        subForm_soporte_papel: false,
        subForm_soporte_electronico: false,
        subForm_extensiones: '',
        subForm_retencion_gestion: '',
        subForm_retencion_central: '',
        subForm_disposicion_final: '',
        subForm_reproduccion_tecnica: '',
        subForm_procedimiento: '',
        subForm_nuevoTipoDoc: '',
        subForm_tiposDocumentales: [],
        
        nuevoTipoDoc: '',
        tiposDocumentales: [],
        procedimiento: '',

        mostrarModalPreview: false,
        mostrarModalNuevoCatalogo: false,
        guardandoCatalogo: false,
        tabCatalogo: 'crear',
        serieEditandoCod: null,
        serieEditandoNuevoCod: '',
        serieEditandoNuevoNom: '',
        nuevoCat_serieCod: '',
        nuevoCat_serieNom: '',
        nuevoCat_incluirSub: false,
        nuevoCat_subCod: '',
        nuevoCat_subNom: '',
        mostrarModalEditar: false,
        edit_id: '',
        edit_codigo: '',
        edit_nombre: '',
        edit_papel: false,
        edit_elec: false,
        edit_ext: '',
        edit_ret_g: '',
        edit_ret_c: '',
        edit_disp: '',
        edit_rep: '',
        edit_proc: '',
        edit_nivel: '',

        // Estado del Modal para Agregar Subserie Directa
        mostrarModalNuevaSubserieDirecta: false,
        modalSub_serieId: null,
        modalSub_serieCodigo: '',
        modalSub_serieNombre: '',
        modalSub_subseriesCatalogo: [],
        modalSub_codigo: '',
        modalSub_nombre: '',
        modalSub_soporte_papel: false,
        modalSub_soporte_electronico: false,
        modalSub_extensiones: '',
        modalSub_retencion_gestion: '',
        modalSub_retencion_central: '',
        modalSub_disposicion_final: '',
        modalSub_reproduccion_tecnica: '',
        modalSub_procedimiento: '',
        modalSub_nuevoTipoDoc: '',
        modalSub_tipos: [],

        abrirModalNuevaSubserieDirecta(serie, consecutivoSugerido) {
            if (!serie) return;
            this.modalSub_serieId = serie.id;
            this.modalSub_serieCodigo = serie.codigo || '';
            this.modalSub_serieNombre = serie.nombre || '';

            // Buscar subseries en el catálogo para esta serie específica
            const sCat = (this.catalogo.series || []).find(s => 
                this.formatearCodigo(s.codigo) === (serie.codigo || '') || (s.nombre && s.nombre.toUpperCase() === (serie.nombre || '').toUpperCase())
            );
            this.modalSub_subseriesCatalogo = (sCat && sCat.subseries) ? sCat.subseries : [];

            this.modalSub_codigo = `${serie.codigo}.${consecutivoSugerido || 1}`;
            this.modalSub_nombre = '';
            this.modalSub_soporte_papel = false;
            this.modalSub_soporte_electronico = false;
            this.modalSub_extensiones = '';
            this.modalSub_retencion_gestion = '';
            this.modalSub_retencion_central = '';
            this.modalSub_disposicion_final = '';
            this.modalSub_reproduccion_tecnica = '';
            this.modalSub_procedimiento = '';
            this.modalSub_nuevoTipoDoc = '';
            this.modalSub_tipos = [];
            this.mostrarModalNuevaSubserieDirecta = true;
        },

        alSeleccionarSubserieEnModalSub(catIdx) {
            if (catIdx === '' || !this.modalSub_subseriesCatalogo[catIdx]) return;
            const subCat = this.modalSub_subseriesCatalogo[catIdx];
            const pref = this.prefijoOficina;
            let cod = subCat.codigo || '';
            if (pref && !cod.startsWith(pref + '.')) {
                if (this.modalSub_serieCodigo && !cod.startsWith(this.modalSub_serieCodigo + '.')) {
                    cod = `${this.modalSub_serieCodigo}.${cod}`;
                } else {
                    cod = `${pref}.${cod}`;
                }
            }
            this.modalSub_codigo = cod;
            this.modalSub_nombre = subCat.nombre;
        },

        agregarTipoAModalSub() {
            const val = (this.modalSub_nuevoTipoDoc || '').trim();
            if (!val) return;
            this.modalSub_tipos.push({
                nombre: this.toTitleCase(val),
                soporte_papel: false,
                soporte_electronico: false,
                extensiones: ''
            });
            this.modalSub_nuevoTipoDoc = '';
        },

        eliminarTipoDeModalSub(idx) {
            this.modalSub_tipos.splice(idx, 1);
        },

        prepararEnvioModalSubserie(e) {
            const cod = (this.modalSub_codigo || '').trim();
            const nom = (this.modalSub_nombre || '').trim();
            if (!cod || !nom) {
                alert('El código y el nombre de la subserie son obligatorios.');
                e.preventDefault();
                return;
            }
        },

        abrirModalEditarItem(item) {
            if (!item) return;
            this.edit_id = item.id;
            this.edit_codigo = item.codigo || '';
            this.edit_nombre = item.nombre || '';
            this.edit_papel = !!item.soporte_papel;
            this.edit_elec = !!item.soporte_electronico;
            this.edit_ext = item.extensiones || '';
            this.edit_ret_g = item.retencion_gestion !== undefined ? item.retencion_gestion : 0;
            this.edit_ret_c = item.retencion_central !== undefined ? item.retencion_central : 0;
            this.edit_disp = item.disposicion_final || '';
            this.edit_rep = item.reproduccion_tecnica || '';
            this.edit_proc = item.procedimiento || '';
            this.edit_nivel = item.nivel || 'REGISTRO';
            this.mostrarModalEditar = true;
        },

        abrirModalEditar(id, cod, nom, papel, elec, ext, ret_g, ret_c, disp, rep, proc, nivel) {
            this.edit_id = id;
            this.edit_codigo = cod || '';
            this.edit_nombre = nom || '';
            this.edit_papel = !!papel;
            this.edit_elec = !!elec;
            this.edit_ext = ext || '';
            this.edit_ret_g = ret_g || 0;
            this.edit_ret_c = ret_c || 0;
            this.edit_disp = disp || '';
            this.edit_rep = rep || '';
            this.edit_proc = proc || '';
            this.edit_nivel = nivel || 'REGISTRO';
            this.mostrarModalEditar = true;
        },

        modoVistaContenido: 'acordeon',
        seriesAbiertas: {},
        toggleSerie(id) {
            this.seriesAbiertas[id] = !this.seriesAbiertas[id];
        },
        expandirTodasSeries() {
            const obj = {};
            
            this.seriesAbiertas = obj;
        },
        colapsarTodasSeries() {
            this.seriesAbiertas = {};
        },

        erroresValidacion: [],
        erroresCampos: {},
        
        get series() {
            return (this.catalogo && this.catalogo.series) ? this.catalogo.series : [];
        },
        get prefijoOficina() {
            return (this.catalogo && this.catalogo.prefijo) ? this.catalogo.prefijo : '';
        },
        get subseriesCatalogoActuales() {
            if (this.serieSeleccionadaIdx === '' || !this.series[this.serieSeleccionadaIdx]) return [];
            return this.series[this.serieSeleccionadaIdx].subseries || [];
        },
        
        formatearCodigo(codBase) {
            const pref = this.prefijoOficina;
            if (!pref || !codBase) return codBase || '';
            return codBase.startsWith(pref + '.') ? codBase : (pref + '.' + codBase);
        },
        
        alSeleccionarSerie() {
            if (this.serieSeleccionadaIdx === '') {
                this.serieCodigo = '';
                this.serieNombre = '';
                this.tieneSubserie = false;
                this.subseries = [];
                this.limpiarSubForm();
                return;
            }
            const s = this.series[this.serieSeleccionadaIdx];
            if (!s) return;
            
            this.serieCodigo = this.formatearCodigo(s.codigo);
            this.serieNombre = s.nombre;
            
            if (s.subseries && s.subseries.length > 0) {
                this.tieneSubserie = true;
                this.limpiarSubForm();
            } else {
                this.tieneSubserie = false;
                this.subseries = [];
                this.limpiarSubForm();
            }
        },
        
        alCambiarTieneSubserie() {
            if (!this.tieneSubserie) {
                this.subseries = [];
                this.limpiarSubForm();
            } else {
                this.limpiarSubForm();
            }
        },

        limpiarSubForm() {
            this.subForm_editandoIdx = null;
            this.subForm_codigo = '';
            this.subForm_nombre = '';
            this.subForm_soporte_papel = false;
            this.subForm_soporte_electronico = false;
            this.subForm_extensiones = '';
            this.subForm_retencion_gestion = '';
            this.subForm_retencion_central = '';
            this.subForm_disposicion_final = '';
            this.subForm_reproduccion_tecnica = '';
            this.subForm_procedimiento = '';
            this.subForm_nuevoTipoDoc = '';
            this.subForm_tiposDocumentales = [];

            if (this.serieCodigo) {
                const numSub = this.subseries.length + 1;
                this.subForm_codigo = `${this.serieCodigo}.${numSub}`;
            }
        },

        alSeleccionarSubserieEnForm(catIdx) {
            if (catIdx === '' || !this.subseriesCatalogoActuales[catIdx]) return;
            const subCat = this.subseriesCatalogoActuales[catIdx];
            const sActual = (this.serieSeleccionadaIdx !== '' && this.series[this.serieSeleccionadaIdx]) ? this.series[this.serieSeleccionadaIdx] : null;
            const pref = this.prefijoOficina;
            let cod = subCat.codigo || '';
            if (pref && !cod.startsWith(pref + '.')) {
                if (sActual && cod.startsWith(sActual.codigo + '.')) {
                    cod = pref + '.' + cod;
                } else if (sActual) {
                    cod = pref + '.' + sActual.codigo + '.' + cod;
                } else {
                    cod = pref + '.' + cod;
                }
            }
            this.subForm_codigo = cod;
            this.subForm_nombre = subCat.nombre;
        },

        toTitleCase(str) {
            if (!str) return '';
            return str.replace(/[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+/g, (w) => w.charAt(0).toUpperCase() + w.substr(1).toLowerCase());
        },

        agregarTipoASubForm() {
            const val = (this.subForm_nuevoTipoDoc || '').trim();
            if (!val) return;
            this.subForm_tiposDocumentales.push({
                nombre: this.toTitleCase(val),
                soporte_papel: false,
                soporte_electronico: false,
                extensiones: ''
            });
            this.subForm_nuevoTipoDoc = '';
        },

        eliminarTipoDeSubForm(tIdx) {
            this.subForm_tiposDocumentales.splice(tIdx, 1);
        },

        guardarSubserieEnLista() {
            const cod = (this.subForm_codigo || '').trim();
            const nom = (this.subForm_nombre || '').trim();
            if (!cod || !nom) {
                alert('El código y el nombre de la subserie son obligatorios.');
                return;
            }

            const subObj = {
                codigo: cod,
                nombre: this.toTitleCase(nom),
                soporte_papel: !!this.subForm_soporte_papel,
                soporte_electronico: !!this.subForm_soporte_electronico,
                extensiones: this.subForm_extensiones || '',
                retencion_gestion: this.subForm_retencion_gestion !== '' ? this.subForm_retencion_gestion : 0,
                retencion_central: this.subForm_retencion_central !== '' ? this.subForm_retencion_central : 0,
                disposicion_final: this.subForm_disposicion_final || '',
                reproduccion_tecnica: this.subForm_reproduccion_tecnica || '',
                procedimiento: this.subForm_procedimiento || '',
                tipos_documentales: JSON.parse(JSON.stringify(this.subForm_tiposDocumentales))
            };

            if (this.subForm_editandoIdx !== null && this.subForm_editandoIdx >= 0) {
                this.subseries[this.subForm_editandoIdx] = subObj;
            } else {
                this.subseries.push(subObj);
            }

            this.limpiarSubForm();
        },

        editarSubserieDeLista(idx) {
            const s = this.subseries[idx];
            if (!s) return;
            this.subForm_editandoIdx = idx;
            this.subForm_codigo = s.codigo || '';
            this.subForm_nombre = s.nombre || '';
            this.subForm_soporte_papel = !!s.soporte_papel;
            this.subForm_soporte_electronico = !!s.soporte_electronico;
            this.subForm_extensiones = s.extensiones || '';
            this.subForm_retencion_gestion = s.retencion_gestion !== undefined ? s.retencion_gestion : '';
            this.subForm_retencion_central = s.retencion_central !== undefined ? s.retencion_central : '';
            this.subForm_disposicion_final = s.disposicion_final || '';
            this.subForm_reproduccion_tecnica = s.reproduccion_tecnica || '';
            this.subForm_procedimiento = s.procedimiento || '';
            this.subForm_nuevoTipoDoc = '';
            this.subForm_tiposDocumentales = JSON.parse(JSON.stringify(s.tipos_documentales || []));

            this.$nextTick(() => {
                if (this.$refs.formularioSubserie) {
                    this.$refs.formularioSubserie.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            });
        },

        cancelarEdicionSubForm() {
            this.limpiarSubForm();
        },

        eliminarSubserieDeLista(idx) {
            this.subseries.splice(idx, 1);
            if (this.subForm_editandoIdx === idx) {
                this.limpiarSubForm();
            } else if (this.subForm_editandoIdx !== null && this.subForm_editandoIdx > idx) {
                this.subForm_editandoIdx--;
            }
        },

        cargarTodasLasSubseriesDelCatalogo() {
            const list = this.subseriesCatalogoActuales;
            if (!list || list.length === 0) return;
            const sActual = (this.serieSeleccionadaIdx !== '' && this.series[this.serieSeleccionadaIdx]) ? this.series[this.serieSeleccionadaIdx] : null;
            const pref = this.prefijoOficina;
            
            list.forEach(catSub => {
                let cod = catSub.codigo || '';
                if (pref && !cod.startsWith(pref + '.')) {
                    if (sActual && cod.startsWith(sActual.codigo + '.')) {
                        cod = pref + '.' + cod;
                    } else if (sActual) {
                        cod = pref + '.' + sActual.codigo + '.' + cod;
                    } else {
                        cod = pref + '.' + cod;
                    }
                }
                const existe = this.subseries.some(s => s.codigo === cod);
                if (!existe) {
                    this.subseries.push({
                        codigo: cod,
                        nombre: catSub.nombre,
                        soporte_papel: false,
                        soporte_electronico: false,
                        extensiones: '',
                        retencion_gestion: '',
                        retencion_central: '',
                        disposicion_final: '',
                        reproduccion_tecnica: '',
                        procedimiento: '',
                        tipos_documentales: []
                    });
                }
            });
            this.limpiarSubForm();
        },
        
        agregarTipoDoc() {
            const val = this.nuevoTipoDoc.trim();
            if (val.length === 0) return;
            this.tiposDocumentales.push({
                nombre: this.toTitleCase(val),
                soporte_papel: false,
                soporte_electronico: false,
                extensiones: ''
            });
            this.nuevoTipoDoc = '';
            this.$nextTick(() => {
                if (this.$refs.inputTipoDoc) this.$refs.inputTipoDoc.focus();
            });
        },
        
        eliminarTipoDoc(idx) {
            this.tiposDocumentales.splice(idx, 1);
        },

        ordenarTiposConsecutivoSerieSimple() {
            this.tiposDocumentales.sort((a, b) => a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' }));
        },

        renderSoporte(papel, elec, ext) {
            let res = [];
            if (papel) res.push('PAPEL');
            if (elec) res.push(ext || 'ELEC');
            return res.join(' / ') || 'PAPEL';
        },

        abrirModalNuevaSerieSubserie(tab = 'crear') {
            this.tabCatalogo = tab;
            this.serieEditandoCod = null;
            this.nuevoCat_serieCod = '';
            this.nuevoCat_serieNom = '';
            this.nuevoCat_incluirSub = false;
            this.nuevoCat_subCod = '';
            this.nuevoCat_subNom = '';
            this.mostrarModalNuevoCatalogo = true;
        },

        iniciarEdicionSerie(s) {
            this.serieEditandoCod = s.codigo;
            this.serieEditandoNuevoCod = s.codigo;
            this.serieEditandoNuevoNom = s.nombre;
        },

        async guardarEdicionSerie(s) {
            const nuevoCod = this.serieEditandoNuevoCod.trim();
            const nuevoNom = this.serieEditandoNuevoNom.trim();
            if (!nuevoCod || !nuevoNom) {
                alert('El código y el nombre son obligatorios.');
                return;
            }
            try {
                const resp = await fetch('/api/ccd/actualizar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        oficina: this.oficinaProductora,
                        codigo_actual: s.codigo,
                        nuevo_codigo: nuevoCod,
                        nuevo_nombre: nuevoNom
                    })
                });
                const res = await resp.json();
                if (res.ok && res.catalogo) {
                    this.catalogo = res.catalogo;
                    this.serieEditandoCod = null;
                } else {
                    alert('Error actualizando serie: ' + (res.error || 'Desconocido'));
                }
            } catch (err) {
                alert('Error de conexión: ' + err.message);
            }
        },

        async eliminarSerieCatalogo(s) {
            if (!confirm(`¿Estás seguro de eliminar la serie '${s.nombre}' del catálogo?`)) return;
            try {
                const resp = await fetch('/api/ccd/eliminar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        oficina: this.oficinaProductora,
                        codigo_serie: s.codigo
                    })
                });
                const res = await resp.json();
                if (res.ok && res.catalogo) {
                    this.catalogo = res.catalogo;
                } else {
                    alert('Error eliminando serie: ' + (res.error || 'Desconocido'));
                }
            } catch (err) {
                alert('Error de conexión: ' + err.message);
            }
        },

        async guardarNuevaSerieEnCatalogo() {
            const sCod = this.nuevoCat_serieCod.trim();
            const sNom = this.nuevoCat_serieNom.trim();
            if (!sNom) {
                alert('Por favor ingresa el nombre de la serie.');
                return;
            }

            if (this.nuevoCat_incluirSub && !this.nuevoCat_subNom.trim()) {
                alert('Por favor ingresa el nombre de la subserie.');
                return;
            }

            this.guardandoCatalogo = true;
            try {
                const resp = await fetch('/api/ccd/guardar_personalizado', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        oficina: this.oficinaProductora,
                        serie_codigo: sCod,
                        serie_nombre: sNom,
                        subserie_codigo: this.nuevoCat_incluirSub ? this.nuevoCat_subCod.trim() : '',
                        subserie_nombre: this.nuevoCat_incluirSub ? this.nuevoCat_subNom.trim() : ''
                    })
                });
                const res = await resp.json();
                if (res.ok && res.catalogo) {
                    this.catalogo = res.catalogo;
                    this.mostrarModalNuevoCatalogo = false;
                    
                    // Buscar la serie recién guardada en el catálogo actualizado
                    const serieCreada = (this.catalogo.series || []).find(s => 
                        s.nombre.toUpperCase() === sNom.toUpperCase() || (sCod && s.codigo === sCod)
                    );
                    
                    if (serieCreada) {
                        this.serieCodigo = this.formatearCodigo(serieCreada.codigo);
                        this.serieNombre = serieCreada.nombre.toUpperCase();
                        
                        if (this.nuevoCat_incluirSub && this.nuevoCat_subNom) {
                            this.tieneSubserie = true;
                            this.subseries = [];
                            const subCreada = (serieCreada.subseries || []).find(sub => 
                                sub.nombre.toUpperCase() === this.nuevoCat_subNom.trim().toUpperCase()
                            );
                            this.subseries.push({
                                codigo: subCreada ? subCreada.codigo : (this.nuevoCat_subCod || `${serieCreada.codigo}.1`),
                                nombre: this.nuevoCat_subNom.trim(),
                                soporte_papel: false,
                                soporte_electronico: false,
                                extensiones: '',
                                retencion_gestion: '',
                                retencion_central: '',
                                disposicion_final: '',
                                reproduccion_tecnica: '',
                                procedimiento: '',
                                tipos_documentales: []
                            });
                            this.limpiarSubForm();
                        }
                    } else {
                        this.serieCodigo = this.formatearCodigo(sCod || '1');
                        this.serieNombre = sNom.toUpperCase();
                    }
                } else {
                    alert('Error guardando en el catálogo: ' + (res.error || 'Desconocido'));
                }
            } catch (err) {
                alert('Error de conexión al guardar en catálogo: ' + err.message);
            } finally {
                this.guardandoCatalogo = false;
            }
        },

        abrirVistaPrevia() {
            this.validarCampos();
            this.mostrarModalPreview = true;
        },

        validarCampos() {
            this.erroresValidacion = [];
            this.erroresCampos = {};

            if (!this.serieCodigo.trim()) {
                this.erroresValidacion.push('El código de la Serie es obligatorio.');
                this.erroresCampos.serieCodigo = true;
                this.erroresCampos.serie = true;
            }
            if (!this.serieNombre.trim()) {
                this.erroresValidacion.push('El nombre de la Serie es obligatorio.');
                this.erroresCampos.serieNombre = true;
                this.erroresCampos.serie = true;
            }

            if (this.tieneSubserie) {
                if (this.subseries.length === 0) {
                    this.erroresValidacion.push('Indicaste que la serie contiene subseries, pero no has agregado ninguna subserie.');
                }
                this.subseries.forEach((s, idx) => {
                    if (!s.codigo.trim() || !s.nombre.trim()) {
                        this.erroresValidacion.push(`La Subserie #${idx + 1} debe tener código y nombre definidos.`);
                        this.erroresCampos['subserie_' + idx] = true;
                    }
                });
            }

            return this.erroresValidacion.length === 0;
        },

        enviarFormulario() {
            if (!this.validarCampos()) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }

            const formElem = this.$refs.formularioTRD || document.querySelector('form');
            let hidden = formElem.querySelector('input[name="estructura_arbol_json"]');
            if (!hidden) {
                hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = 'estructura_arbol_json';
                formElem.appendChild(hidden);
            }
            hidden.value = JSON.stringify(this.construirArbol());
            formElem.submit();
        },

        construirArbol() {
            return {
                serie_codigo: this.serieCodigo,
                serie_nombre: this.serieNombre,
                serie_soporte_papel: this.serie_soporte_papel,
                serie_soporte_electronico: this.serie_soporte_electronico,
                serie_extensiones: this.serie_extensiones,
                serie_retencion_gestion: this.serie_retencion_gestion,
                serie_retencion_central: this.serie_retencion_central,
                serie_disposicion_final: this.serie_disposicion_final,
                serie_reproduccion_tecnica: this.serie_reproduccion_tecnica,
                tiene_subserie: this.tieneSubserie,
                procedimiento: this.procedimiento,
                tipos_documentales: this.tiposDocumentales,
                subseries: this.subseries.map(s => ({
                    codigo: s.codigo,
                    nombre: s.nombre,
                    soporte_papel: s.soporte_papel,
                    soporte_electronico: s.soporte_electronico,
                    extensiones: s.extensiones,
                    retencion_gestion: s.retencion_gestion,
                    retencion_central: s.retencion_central,
                    disposicion_final: s.disposicion_final,
                    reproduccion_tecnica: s.reproduccion_tecnica,
                    procedimiento: s.procedimiento,
                    tipos_documentales: s.tipos_documentales || []
                }))
            };
        },
        
        limpiarTodo() {
            this.serieSeleccionadaIdx = '';
            this.serieCodigo = '';
            this.serieNombre = '';
            this.serie_soporte_papel = false;
            this.serie_soporte_electronico = false;
            this.serie_extensiones = '';
            this.serie_retencion_gestion = '';
            this.serie_retencion_central = '';
            this.serie_disposicion_final = '';
            this.serie_reproduccion_tecnica = '';
            
            this.tieneSubserie = false;
            this.subseries = [];
            this.limpiarSubForm();
            
            this.nuevoTipoDoc = '';
            this.tiposDocumentales = [];
            this.procedimiento = '';
            this.erroresValidacion = [];
            this.erroresCampos = {};
        }
    };
}
