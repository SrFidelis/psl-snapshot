# PSL SNAPSHOT v2.1 - 3Dview Addon - Blender 2.8
#
# THIS SCRIPT IS LICENSED UNDER GPL, 
# please read the license block.
#
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "PSL_SnapShot",
    "author": "Vinícius Fidelis Pk, Canal CGI Brasil",
    "tracker_url": "https://bit.ly/308d9wY",
    "wiki_url": "https://bit.ly/2xD4cke",
    "version": (2, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Nkey Panel > Animate -> PSL SnapShot",
    "description": "Make SnapShots from Animated Meshes",
    "warning": "",
    "support": "COMMUNITY",
    "category": "Animation"}

import bpy
import os

prefixpsl = 'PSL_'

snapshotSource = prefixpsl + 'snapshotSource'
snapshotInstances = prefixpsl + 'snapshotInstances'

nameMaterialSlot   = prefixpsl + 'SNAPSHOT_SLOT'
nameMaterialGray   = prefixpsl + 'SNAPSHOT_GRAY'
nameMaterialBlack  = prefixpsl + 'SNAPSHOT_BLACK'
nameMaterialCustom = prefixpsl + 'SNAPSHOT_CUSTOM'

nameObjectPrefix = prefixpsl + "SNAPSHOT_"
nameEmptyDad = prefixpsl + "SNAPSHOT_DAD"

def initializeMaterials(): #DEFININDO FUNÇÃO QUE INICIA OS MATERIAIS
    try:
        materialgray = bpy.data.materials[nameMaterialGray]
    except:
        materialgray = bpy.data.materials.new(nameMaterialGray)
        bpy.data.materials[nameMaterialGray].diffuse_color = (0.35884, 0.35884, 0.35884, 1)
        
    try:
        materialblack = bpy.data.materials[nameMaterialBlack]
    except:
        materialblack = bpy.data.materials.new(nameMaterialBlack)
        bpy.data.materials[nameMaterialGray].diffuse_color = (0, 0, 0, 1)      
        
    try:
        materialcustom = bpy.data.materials[nameMaterialCustom]
    except:
        materialcustom = bpy.data.materials.new(nameMaterialCustom)
        bpy.data.materials[nameMaterialCustom].diffuse_color = (1, 0, 0, 1)


def initializeSnpashotGroups(): #DEFININDO FUNÇÃO QUE CRIA AS COLEÇÕES INVÉS DE GRUPOS
    try: 
        group = bpy.data.collections[snapshotSource]       
    except:
        coll = bpy.data.collections.new(snapshotSource)
        bpy.context.scene.collection.children.link(coll)
        
    try:
        group = bpy.data.collections[snapshotInstances]    
    except:
        coll = bpy.data.collections.new(snapshotInstances)
        bpy.context.scene.collection.children.link(coll)

        
def createEmptyGroup(): #DEFININDO FUNÇÃO QUE CRIA O PAI
    actual_selected = bpy.context.selected_objects[:]
    try:
        dad = bpy.data.objects[nameEmptyDad]
    except:            
        bpy.ops.object.add(type='EMPTY', enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0))
        bpy.context.object.name = nameEmptyDad

    for object in bpy.data.objects:
        if object in actual_selected:
            object.select_set(state=True, view_layer=None)
        else:
            object.select_set(state=False, view_layer=None)
            

def initializePSLsnapshot(): #DEFININDO FUNÇÃO PARA INICIAR O PSL

    actual_object = ""        
    actual_mode = bpy.context.mode 
    scn = bpy.context.scene
    
    try: 
        if actual_mode == 'POSE':
            bones_selection = bpy.context.selected_pose_bones_from_active_object[:]
            actual_selection = bpy.context.selected_objects[0].name
        else:
            actual_selection = bpy.context.selected_objects[0].name
            actual_object = bpy.context.active_object.name
    except:
        pass
        
    if actual_mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
                  
    bpy.ops.object.select_pattern(pattern="", extend=False)
    bpy.context.view_layer.objects.active = None
    
    initializeMaterials()
    initializeSnpashotGroups()
    createEmptyGroup() 
    
    bpy.ops.object.select_pattern(pattern="", extend=False)
    bpy.context.view_layer.objects.active = None
        
    try: 
        if actual_mode == 'POSE':
            bpy.ops.object.select_pattern(pattern=actual_selection, extend=False)
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
            bpy.ops.object.mode_set(mode='POSE')
            for bone in bones_selection:
                n =+ 1
                id = bones_selection.count(n)
                bone = bones_selecion[id].name
                bpy.ops.object.select_pattern(pattern=bone, extend=False)
        else:
            #scn.objects.active = scn.objects[actual_object]
            bpy.context.view_layer.objects.active = scn.objects[actual_object]
            bpy.context.scene.objects[actual_object]
            if len(actual_selection) != 0:
                bpy.ops.object.select_pattern(pattern=actual_object, extend=False)
                       
    except:
        pass
    
       
def addObjectsToSource(context): # DEFININDO FUNÇÃO PARA ADICIONAR OBJETO SELECIONADO PARA A COLEÇÃO SOURCE
    objects_to_add = [obj.name for obj in bpy.context.selected_objects if obj.type == 'MESH']  
    
    scn = bpy.context.scene  
    
    for name in objects_to_add:  
        context.view_layer.objects.active = scn.objects[name]  
        bpy.ops.object.collection_link(collection=snapshotSource)
        
            
class PSL_AddToSourceGroup(bpy.types.Operator): # CLASSE OPERADOR PARA ADICIONAR O ELEMENTO PARA A COLEÇÃO SOURCE
    bl_idname = "object.addtosourcegroup"
    bl_label = "Add To Source Group"
    bl_description = "Add element to source group"

    @classmethod
    def poll(cls, context):
        sel_objects = bpy.context.selected_objects
        if len(sel_objects) == 0 :
            return False
        all_mesh = True
        for object in sel_objects:
            if object.type != 'MESH':
                all_mesh = False
                return all_mesh
        return all_mesh

    def execute(self, context): 
        try:
            #initializePSLsnapshot()    
            addObjectsToSource(context)
        except:
            self.report(type={'ERROR'}, message="Error adding to the source" ) 
        return {'FINISHED'}
    
class PSL_DeleteFromSourceGroup(bpy.types.Operator): # OPERADOR PARA REMOVER O ELEMENTO DA COLEÇÃO SOURCE
    bl_idname = "object.deletefromsourcegroup"
    bl_label = "Delete from Source Group"
    bl_description = "Delete element from source group"

    @classmethod
    def poll(cls, context):
        try:
            objects = bpy.data.collections[snapshotSource].objects
            sel_objects = context.selected_objects            
            for each_object in objects:
                is_there = False
                for each_selobject in sel_objects:
                    if each_selobject == each_object:
                        is_there = True
                        return is_there
            return is_there
        except:
            return False
        return False
        return True #context.active_object is not None

    def execute(self, context): 
        try:
            sel_objects = bpy.context.selected_objects
            source_Group = bpy.data.collections[snapshotSource]
            
            for selobject in sel_objects:
                try:
                   source_Group.objects.unlink(selobject)
                except:
                    raise
                    
        except:
            self.report(type={'ERROR'}, message="Error removing from source" ) 
        return {'FINISHED'}

def changeGroup (context, object): #DEFININDO FUNÇÃO PARA MUDAR OBJETO ATIVADO PARA A COLEÇÃO INSTANCES  
    scn = bpy.context.scene  

    bpy.context.view_layer.objects.active = scn.objects[object.name]
    bpy.ops.object.collection_link(collection=snapshotInstances)
    
    
def applyMaterial (context, object, materialname): #DEFININDO FUNÇÃO PARA APLICAR MATERIAL NO OBJETO
    scn = bpy.context.scene

    bpy.context.view_layer.objects.active = scn.objects[object.name]
    bpy.ops.object.material_slot_remove()
    bpy.ops.object.material_slot_add()
    slot = bpy.context.object.material_slots[0]
    slot.material = bpy.data.materials[materialname]

def exportImportObj(object): # FUNÇÃO PARA EXPORTAR E IMPORTAR O OBJETO
    newObject = None
    print("**************************" + object.name)
    

    filepathbas = '/tmp/'
    filepathobj = filepathbas+'psl_snapshot_temp.obj'
    filepathmtl = filepathbas+'psl_snapshot_temp.mtl'
    
    bpy.ops.object.select_pattern(pattern="", extend=False)
    bpy.ops.object.select_pattern(pattern=object.name, extend=False)

    bpy.ops.export_scene.obj(filepath=filepathobj, use_selection=True, use_materials=False)
    bpy.ops.import_scene.obj(filepath=filepathobj)

    default_material = bpy.data.materials['Default OBJ']
    bpy.data.materials.remove(default_material)
    
    try:
        os.remove(filepathobj)
    except:
        pass
    try:
        os.remove(filepathmtl)
    except:
        pass
    return newObject

 
def duplicateObjects(context, material): #FUNÇÃO PARA DUPLICAR OS OBJETOS DA COLEÇAO SOURCE
    objects = bpy.data.collections[snapshotSource].objects
    scn = bpy.context.scene  
    
    for eachobject in objects:
        if eachobject in bpy.context.visible_objects:
            
            exportImportObj(eachobject)  
            newobject = bpy.context.selected_objects[0]
            newobject.name = nameObjectPrefix + newobject.name.split(".")[0] + "__" + str(scn.frame_current)
            
            changeGroup(context, newobject)
                        
            if material == "GRAY":
                applyMaterial(context, newobject, nameMaterialGray)
            if material == "BLACK":
                applyMaterial(context, newobject, nameMaterialBlack)
            if material == "CUSTOM":
                applyMaterial(context, newobject, nameMaterialCustom) 
            
            newobject.parent = bpy.data.objects[nameEmptyDad]   
            
            decimate = newobject.modifiers.new(name="decimate", type='DECIMATE')
            decimate.ratio = scn.psl_decimate_ratio
            

def generateSnapshot(self, context): #DEFININDO FUNÇÃO PARA GERAR SNAPSHOTS
    selected_objects = bpy.context.selected_objects[:] 
    actual_object = ""        
    actual_mode = bpy.context.mode 
    scn = bpy.context.scene 
    
    try:         
        actual_object = bpy.context.active_object.name
    except:
        pass
    
    if bpy.context.mode != 'OBJECT':
         bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.object.select_pattern(pattern="", extend=False)
    bpy.context.view_layer.objects.active = None
    
    material = scn.psl_snapshot_material
    duplicateObjects(context, material)

    objects = scn.objects
    
    for object in objects:
        if object in selected_objects:
            object.select_set(state=True, view_layer=None)
        else:
            object.select_set(state=False, view_layer=None)
    
    try:   
        bpy.context.view_layer.objects.active = scn.objects[actual_object]   
        bpy.ops.object.mode_set(mode=actual_mode)       
    except:
        pass

class PSL_MakeSnapshot(bpy.types.Operator): #CLASSE OPERADORA PARA FAZER O SNAPSHOT
    '''Tooltip'''
    bl_idname = "object.make_snapshot"
    bl_label = "Make Snapshot"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Make Snapshot!"
        
    material = bpy.props.StringProperty(name="material", description="Material", default="GRAY")

    @classmethod
    def poll(cls, context):
        try:
            objects = bpy.data.collections[snapshotSource].objects
            if len(objects) > 0:
                return True
            else:
                return False
        except:
            return False
        return False

    def execute(self, context):      
        try:
            scn = bpy.context.scene
            if not scn.psl_generate_all:    
                CleanExistingSnapshot(context)
                generateSnapshot(self, context)       
            else:        
                last_frame = False    
                CleanAllSnapshots(context)
                scn.frame_set(scn.psl_snapshot_start)
                generateSnapshot(self, context)
                
                while (not last_frame) and (scn.frame_current < scn.psl_snapshot_end):
                    actual_frame = scn.frame_current
                    
                    bpy.ops.screen.keyframe_jump(next=True)
                    if actual_frame != scn.frame_current:
                        generateSnapshot(self, context)
                    else:
                        last_frame = True
    
            
            if not scn.psl_generate_all and scn.psl_jump_next_frame:
                bpy.ops.screen.keyframe_jump(next=True)   
        except:
            self.report(type={'ERROR'}, message="Error making snapshot" ) 
        return {'FINISHED'}
    
    
def CleanExistingSnapshot(context): #DEFININDO FUNÇÃO PARA APAGAR A SNAPSHOT EXISTENTE NO FRAME

    scn = bpy.context.scene
          
    objects = []
    for object in scn.objects:
        if nameObjectPrefix in object.name:
            end = object.name.split("__")[len(object.name.split("__"))-1]
            endd = end.split(".")[0]
            if str(scn.frame_current) == endd:
                bpy.data.objects.remove(object) 

def CleanAllSnapshots(context): #DEFININDO FUNÇÃO PARA APAGAR TODAS AS SNEPSHOTS EXISTENTES
    
    scn = bpy.context.scene
    objects = bpy.data.collections[snapshotInstances].objects
    
    for object in objects:
        bpy.data.objects.remove(object)
        

class PSL_CleanSnapshots(bpy.types.Operator): #CLASSE OPERADORA PARA CHAMAR A FUNÇÃO DE DELETAR SNAPSHOT DO FRAME ATUAL OU TODOS
    '''Tooltip'''
    bl_idname = "object.clean_snapshots"
    bl_label = "Clean Spanshots"
    bl_description = "Delete Current Frame Snapshot"
    
    all = bpy.props.BoolProperty(name="All", description="Delete all snapshots", default=False)
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context): 
        try:
            if (self.all):        
                CleanAllSnapshots(context)
            
            else:
                CleanExistingSnapshot(context)
                if context.scene.psl_jump_next_frame:
                    bpy.ops.screen.keyframe_jump(next=True) 
            
        except:
            self.report(type={'ERROR'}, message="Error deleting snapshot" )          
        return {'FINISHED'}
    

class PSL_SnapshotVisible(bpy.types.Operator): #CLASSE OPERADORA PARA A VISIBILIDADE DO SNAPSHOT
    bl_idname = "object.snapshot_visible"
    bl_label = "Enable / Disable Visibility Snapshot"
    bl_description = "Show / Hide snapshots"
        
    visible = bpy.props.BoolProperty(name="Visible", description="make visible", default=False)
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:                
                object.hide_viewport = not self.visible
            bpy.types.PSL_SnapshotUI.visible = self.visible
        except:
            self.report(type={'ERROR'}, message="Error while enabling / disabling visibility of the snapshots" )  
        return {'FINISHED'}
 
class PSL_SnapshotRendereable(bpy.types.Operator): #CLASSE OPERADORA PARA A RENDERABILIDADE DO SNAPSHOT
    bl_idname = "object.snapshot_renderable"
    bl_label = "Enable / Disable Render Snapshot"
    bl_description = "Enable / Disable render snapshots"
    
    rendeable = bpy.props.BoolProperty(name="Rendeable", description="make rendeable", default=False)
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:
                object.hide_render = not self.rendeable
            bpy.types.PSL_SnapshotUI.rendeable = self.rendeable   
        except:
            self.report(type={'ERROR'}, message="Error while enabling / disabling render of the snapshots" )                
        return {'FINISHED'}

class PSL_SnapshotSelectable(bpy.types.Operator): #CLASSE OPERADORA PARA A SELECIONABILIDADE DO SNAPSHOT
    bl_idname = "object.snapshot_selectable"
    bl_label = "Select / Deselect snapshot"
    bl_description = "Enable / Disable select snapshots"
    
    selectable = bpy.props.BoolProperty(name="Selectable", description="make selectable", default=False)
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:            
                object.hide_select = not self.selectable      
            bpy.types.PSL_SnapshotUI.selectable = self.selectable
        except:
            self.report(type={'ERROR'}, message="Error while enabling / disabling select of the snapshots" )   
        return {'FINISHED'}    

class PSL_DecimateVisible(bpy.types.Operator): #CLASSE OPERADORA PARA VISIBILIDADE DO DECIMATE
    bl_idname = "object.decimate_visible"
    bl_label = "Enable / Disable visibility decimate"
    bl_description = "Enable / Disable visibility decimate modifier"
        
    visible = bpy.props.BoolProperty(name="Visible", description="make visible", default=True)
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:            
                object.modifiers['decimate'].show_viewport = not self.visible
            bpy.types.PSL_SnapshotUI.visible_decimate = self.visible
        except:
            self.report(type={'ERROR'}, message="Error while enabling / disabling visibility of the decimate" )   
        return {'FINISHED'}
 
class PSL_DecimateRendereable(bpy.types.Operator): #CLASSE OPERADORA PARA A RENDERABILIDADE DO DECIMATE
    bl_idname = "object.decimate_renderable"
    bl_label = "Enable / Disable render of decimate"
    bl_description = "Enable / Disable render decimate modifier"
        
    rendeable = bpy.props.BoolProperty(name="Rendeable", description="make rendeable", default=False)
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:
                object.modifiers['decimate'].show_render = not self.rendeable
            bpy.types.PSL_SnapshotUI.rendeable_decimate = self.rendeable    
        except:
            self.report(type={'ERROR'}, message="Error while enabling / disabling render of the decimate" )                 
        return {'FINISHED'}

class PSL_DecimateUpdate(bpy.types.Operator): #CLASSE OPERADORA PARA ATUALIZAR O CONTROLADOR DE RATIO DO DECIMATE
    bl_idname = "object.decimate_update"
    bl_label = "Update decimate ratio"    
    bl_description = "Update decimate modifier"   
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context): 
        try:
            objects = bpy.data.collections[snapshotInstances].objects
            for object in objects:
                object.modifiers['decimate'].ratio = context.scene.psl_decimate_ratio
        except:
            self.report(type={'ERROR'}, message="Error while updating the decimate" ) 
        return {'FINISHED'}

class PSL_RadioButtonMaterial(bpy.types.Operator):
    bl_idname = "object.pls_rdbmaterial"
    bl_label = "Update radio button material"    
    bl_description = "Select Material"    
    material   = bpy.props.StringProperty(name="material", description="material", default="BLACK")
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):  
        try:       
            scn = context.scene
            scn.psl_snapshot_material = self.material
        except:
            self.report(type={'ERROR'}, message="Error updating material" ) 
        return {'FINISHED'}

class PSL_Snapshot_Initialize(bpy.types.Operator): #OPERADOR PARA INICIAR O PSL
    bl_idname = "object.psl_snp_initialize"
    bl_label = "Initialize"    
    bl_description = "Re/Generate all necesary for the addon "
    
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):  
        try:       
            initializePSLsnapshot()
        except:
            self.report(type={'ERROR'}, message="Error while initializing the addon" ) 
        return {'FINISHED'}
    
class PSL_Snapshot_Turnoff(bpy.types.Operator): #OPERADOR PARA INICIAR O PSL
    bl_idname = "object.psl_snp_turnoff"
    bl_label = "Turn Off"    
    bl_description = "Delete all addon objects"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):  
        try:       
            try:
                CleanAllSnapshots(context)

                empty = bpy.data.objects[nameEmptyDad]
                bpy.data.objects.remove(empty)

                source = bpy.data.collections[snapshotSource]
                bpy.data.collections.remove(source)
            
                instances = bpy.data.collections[snapshotInstances]
                bpy.data.collections.remove(instances)
            except:
                pass
            
            gray = bpy.data.materials[nameMaterialGray]
            bpy.data.materials.remove(gray)
        
            custom = bpy.data.materials[nameMaterialCustom]
            bpy.data.materials.remove(custom)
        
            black = bpy.data.materials[nameMaterialBlack]
            bpy.data.materials.remove(black)
        
        except:
            self.report(type={'ERROR'}, message="Error while turn off the addon") 
        return {'FINISHED'}
        
class PSL_SnapshotUI(bpy.types.Panel): #CLASSE DA APARENCIA NO PROGRAMA
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "PSL SnapShot"
    bl_category = "Animate"
    bl_options = {'DEFAULT_CLOSED'}

    material   = bpy.props.BoolProperty(name="gray_material", description="gray_material", default=False)
    selectable = bpy.props.BoolProperty(name="Selectable", description="make selectable", default=False) 
    rendeable  = bpy.props.BoolProperty(name="Rendeable", description="make rendeable", default=False)
    visible    = bpy.props.BoolProperty(name="Visible", description="make visible", default=False)

    rendeable_decimate  = bpy.props.BoolProperty(name="Rendeable Decimate", description="make rendeable", default=False)
    visible_decimate    = bpy.props.BoolProperty(name="Visible Decimate", description="make visible", default=False)

    def draw(self, context):
        layout = self.layout        
        scn = bpy.context.scene  
        regenerar = False
        try: 
            m1 =  bpy.data.materials[nameMaterialBlack]
            m2 =  bpy.data.materials[nameMaterialGray]
            m3 =  bpy.data.materials[nameMaterialCustom]
        except:
            regenerar = True
        
        if not regenerar:
            #obj operators
            colobjs = layout.column()
            colobjs.label(text="Objs to Snapshot:")
            operator = colobjs.operator("object.addtosourcegroup",text="Add to List",icon='EXPORT')      
            operator = colobjs.operator("object.deletefromsourcegroup",text="Delete from List",icon='X')  
            colobjs.label(text="")
                
            
            #snapshot operator
            
            colsnapshot = layout.row(align=True)
            colsnapshot.label(text="Snapshots") #, icon='GROUP')

            if self.visible :
                operator = colsnapshot.operator("object.snapshot_visible",text="",icon='RESTRICT_VIEW_OFF') 
                operator.visible=False
            else:
                operator = colsnapshot.operator("object.snapshot_visible",text="",icon='RESTRICT_VIEW_ON') 
                operator.visible=True

            if self.selectable:
                operator = colsnapshot.operator("object.snapshot_selectable",text="",icon='RESTRICT_SELECT_OFF') 
                operator.selectable=False
            else:
                operator = colsnapshot.operator("object.snapshot_selectable",text="",icon='RESTRICT_SELECT_ON') 
                operator.selectable=True
                 
            if self.rendeable :
                operator = colsnapshot.operator("object.snapshot_renderable",text="",icon='RESTRICT_RENDER_OFF') 
                operator.rendeable=False
            else:
                operator = colsnapshot.operator("object.snapshot_renderable",text="",icon='RESTRICT_RENDER_ON') 
                operator.rendeable=True
                
            colbuttonsnpshot = layout.row(align=True)  
            colbuttonsnpshot.scale_y = 2
            colbuttonsnpshot.prop ( scn,"psl_jump_next_frame", icon='FF',text="") 
            operator = colbuttonsnpshot.operator("object.make_snapshot",text="Make snapshot",icon='NONE')
            operator = colbuttonsnpshot.operator("object.clean_snapshots",text="",icon='X')  
            operator.all = False
            
            
            layout.separator()
            
            colgekeyscheck = layout.column()
            colgekeyscheck.prop (scn, "psl_generate_all")#, icon ='SCRIPTPLUGINS')
            colgekeys = layout.row(align=True)
            colgekeys.enabled = scn.psl_generate_all
            colgekeys.prop (scn, "psl_snapshot_start") 
            colgekeys.prop (scn, "psl_snapshot_end") 
            
     

            col = layout.row()     
          
            boxcolors = col.box()
            

            if scn.psl_snapshot_material == 'BLACK':
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color1",icon='RADIOBUT_ON',emboss=False)
                operator.material = "BLACK"  
                col1.active = True
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialBlack],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True

                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color2",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "GRAY"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialGray],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True 
                
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color3",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "CUSTOM"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialCustom],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True
                      
            if scn.psl_snapshot_material == 'GRAY':
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color1",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "BLACK"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialBlack],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True
                
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color2",icon='RADIOBUT_ON',emboss=False)
                operator.material = "GRAY"  
                col1.active = True
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialGray],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True 
                
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color3",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "CUSTOM"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialCustom],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True          
            if scn.psl_snapshot_material == 'CUSTOM':
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color1",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "BLACK"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialBlack],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True
                
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color2",icon='RADIOBUT_OFF',emboss=False)
                operator.material = "GRAY"  
                col1.active = False
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialGray],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True 
                
                row = boxcolors.row()
                col1 = row.column()
                operator = col1.operator("object.pls_rdbmaterial",text="Color3",icon='RADIOBUT_ON',emboss=False)
                operator.material = "CUSTOM"  
                col1.active = True
                col2 = row.column()
                col2.prop ( bpy.data.materials[nameMaterialCustom],"diffuse_color",text ="", icon_only=True)   
                col2.enabled = True
                
           
            
            
          
            layout.separator()
           
            rowcleansnapshot = layout.row(align=False)
            rowcleansnapshot.label(text="Optimize Snapshot Meshes:") #, icon='GROUP')

            type_vis = True
            coldecimate = layout.row(align=True)
            coldecimate.prop(scn,"psl_decimate_ratio")
            operator =coldecimate.operator("object.decimate_update",text="",icon='FILE_REFRESH',emboss=type_vis)   
            
            coldecimate.separator()
            
            if self.visible_decimate :
                operator = coldecimate.operator("object.decimate_visible",text="",icon='RESTRICT_VIEW_OFF',emboss=type_vis) 
                operator.visible=False
            else:            
                operator = coldecimate.operator("object.decimate_visible",text="",icon='RESTRICT_VIEW_ON',emboss=type_vis) 
                operator.visible=True           
            
                 
            if self.rendeable_decimate :
                operator = coldecimate.operator("object.decimate_renderable",text="",icon='RESTRICT_RENDER_OFF',emboss=type_vis) 
                operator.rendeable=False
            else:
                #col = col.box()
                operator = coldecimate.operator("object.decimate_renderable",text="",icon='RESTRICT_RENDER_ON',emboss=type_vis) 
                operator.rendeable=True
            
            layout.separator()
            
            rowcleanall = layout.row(align=True)
            
            rowcleanall.scale_y = 1
            operator = rowcleanall.operator("object.clean_snapshots",text="Clean All Snapshots",icon='CANCEL')  
            operator.all = True
            
            rowturnoff = layout.row(align=True)
            
            rowcleanall.scale_y = 1
            operator = rowturnoff.operator("object.psl_snp_turnoff",text="Turn Off PSL",icon='QUIT')
            
            
            # if there aren't elements in source
            num_objects = len(bpy.data.collections[snapshotSource].objects)
            if num_objects == 0 :
                colsnapshot.enabled = False
                boxcolors.enabled = False
                colbuttonsnpshot.enabled = False
                colgekeyscheck.enabled = False
                colgekeys.enabled = False
                coldecimate.enabled = False
                rowcleanall.enabled = False
                rowcleansnapshot.enabled = False
                
                
        else:
            colobjs = layout.column()
            #colobjs.label(text="Objs to Snapshot:")
            operator = colobjs.operator("object.psl_snp_initialize",text="Initialize",icon='NONE')

        
def register():
    # Define properties for the draw setting.
    
    bpy.types.Scene.psl_generate_all = bpy.props.BoolProperty(
        name="Do it in all keyframes",
        description="Generate Snapshots in all Keyframes from start to end",
        default=0)
    bpy.types.Scene.psl_snapshot_start = bpy.props.IntProperty(
        name="Start",
        description="From frame snapshot",
        default=1)    
    bpy.types.Scene.psl_snapshot_end = bpy.props.IntProperty(
        name="End",
        description="To end snapshot",
        default=150)
            
    bpy.types.Scene.psl_jump_next_frame = bpy.props.BoolProperty(
        name="Jump next key-frame",
        description="When on jump to next key-frame after make snapshot",
        default=0)

    bpy.types.Scene.psl_decimate_ratio = bpy.props.FloatProperty(
        name="Decimate Ratio",
        description="Value of the decimate modifier",
        max=1,
        min=0,
        default=1.0)   
    
    bpy.types.Scene.psl_decimate_renderable = bpy.props.BoolProperty(
        name="Render decimate",
        description="Enable / disable renderable decimate",
        default=1)      
    bpy.types.Scene.psl_decimate_visibility = bpy.props.BoolProperty(
        name="Render visualize",
        description="Enable / disable visibility decimate",
        default=1) 
    
    bpy.types.Scene.psl_snapshot_material = bpy.props.StringProperty(
        name="Snapshot Material",
        description="Enable / disable visibility decimate",
        default="BLACK")
        
    bpy.utils.register_class(PSL_AddToSourceGroup)
    bpy.utils.register_class(PSL_DeleteFromSourceGroup)
    bpy.utils.register_class(PSL_MakeSnapshot)
    bpy.utils.register_class(PSL_CleanSnapshots)
    bpy.utils.register_class(PSL_SnapshotRendereable)
    bpy.utils.register_class(PSL_SnapshotSelectable)    
    bpy.utils.register_class(PSL_SnapshotUI)
    bpy.utils.register_class(PSL_SnapshotVisible)
    
    bpy.utils.register_class(PSL_RadioButtonMaterial)

    bpy.utils.register_class(PSL_DecimateVisible)
    bpy.utils.register_class(PSL_DecimateRendereable)  
    bpy.utils.register_class(PSL_DecimateUpdate)
    
    bpy.utils.register_class(PSL_Snapshot_Initialize)
    bpy.utils.register_class(PSL_Snapshot_Turnoff)

def unregister():
    bpy.utils.unregister_class(PSL_AddToSourceGroup)
    bpy.utils.unregister_class(PSL_DeleteFromSourceGroup)
    bpy.utils.unregister_class(PSL_MakeSnapshot)
    bpy.utils.unregister_class(PSL_CleanSnapshots)
    bpy.utils.unregister_class(PSL_SnapshotRendereable)
    bpy.utils.unregister_class(PSL_SnapshotSelectable)  
    bpy.utils.unregister_class(PSL_SnapshotUI)
    bpy.utils.unregister_class(PSL_SnapshotVisible)
    
    bpy.utils.unregister_class(PSL_RadioButtonMaterial)

    bpy.utils.unregister_class(PSL_DecimateVisible)
    bpy.utils.unregister_class(PSL_DecimateRendereable)        
    bpy.utils.unregister_class(PSL_DecimateUpdate)  
    
    bpy.utils.unregister_class(PSL_Snapshot_Initialize)
    bpy.utils.unregister_class(PSL_Snapshot_Turnoff)
    
    del bpy.types.Scene.psl_generate_all
    del bpy.types.Scene.psl_snapshot_start
    del bpy.types.Scene.psl_snapshot_end
    del bpy.types.Scene.psl_jump_next_frame
    del bpy.types.Scene.psl_decimate_ratio
    del bpy.types.Scene.psl_decimate_renderable
    del bpy.types.Scene.psl_decimate_visibility    
    del bpy.types.Scene.psl_snapshot_material
    

if __name__ == "__main__":    
    register()
