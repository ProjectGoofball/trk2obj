import time

def exp_obj1(f, amesh):
    for vert in amesh.wverts:
        wp = vert
        f.write(f"v {wp.x} {wp.y} {-wp.z}\n")

def exp_obj3(f, amesh, base2):
    matdef = materials[amesh.texture]
    udir, vdir = VEC3(), VEC3()
    v0, u0 = 0, 0
    lplane = amesh.planes[0]
    ind = amesh.indices[0]
    while ind < amesh.indices[-1]:
        udir = (lplane.normal % lplane.normal.findAnyPerpendVector()).normalized()
        vdir = lplane.normal % udir
        udir *= matdef.scaleX * amesh.texscale.x
        vdir *= matdef.scaleY * amesh.texscale.y
        u0 = (amesh.textureCenterShift * udir) - 0.5
        v0 = (amesh.textureCenterShift * vdir) - 0.5
        vCount = ind
        ind += 1
        for i in range(vCount):
            tu = (((amesh.verts[ind] * udir) - u0))
            tv = -(((amesh.verts[ind] * vdir) - v0))
            f.write(f"vt {tu} {tv}\n")
            base2 += 1
            ind += 1
        lplane += 1

def exp_obj2(f, amesh, base, b2):
    ind = amesh.indices[0]
    while ind < amesh.indices[-1]:
        vCount = ind
        ind += 1
        f.write("f ")
        for i in range(vCount):
            f.write(f"{ind + base}/{b2} ")
            ind += 1
            b2 += 1
        f.write("\n")
    base += len(amesh.wverts)

def export_scene():
    rawtime = time.time()
    timeinfo = time.localtime(rawtime)
    timebuf = time.strftime("%M_%S", timeinfo)
    str = f"goofball_scene_{timebuf}.mtl"
    str2 = f"goofball_scene_{timebuf}.obj"
    f = open(str, "wb")
    for i in range(len(materials[i].texturefilename)):
        f.write(f"newmtl tex{i}\n")
        f.write("Kd 1.0 1.0 1.0\n")
        f.write("Ka 0.5 0.5 0.5\n")
        f.write(f"map_Kd {materials[i].texturefilename}\n")
    f.close()
    f = open(str2, "wb")
    f.write("# Wavefront OBJ file exported by Goofball Goals\n\n")
    base = 1
    base2 = 1
    index = 0
    name = "b"
    sphere = AMESH()
    sphere.createSphere(3)
    for obj in objs:
        if obj.alive() and obj.triggermanusindex == 0:
            obase2 = base2
            f.write(f"#\n# obj: {name}{index:04d}\n#\n\n")
            for meshi in range(len(obj.ameshes)):
                exp_obj1(f, obj.ameshes[meshi])
            for eli in range(len(obj.ellipdoids)):
                sphere.transform(obj.ellipdoids[eli].wtrans)
                exp_obj1(f, sphere)
            for meshi in range(len(obj.ameshes)):
                exp_obj3(f, obj.ameshes[meshi], base2)
            for eli in range(len(obj.ellipdoids)):
                sphere.transform(obj.ellipdoids[eli].wtrans)
                exp_obj3(f, sphere, base2)
            f.write(f"\ng {name}{index:04d}\ns off\n")
            texture = 0
            if len(obj.ameshes) > 0:
                texture = obj.ameshes[0].texture
            if len(obj.ellipdoids) > 0:
                texture = obj.ellipdoids[0].texture
            f.write("mtllib tt_scene.mtl\n")
            f.write(f"usemtl tex{texture}\n")
            base2 = obase2
            for meshi in range(len(obj.ameshes)):
                amesh = obj.ameshes[meshi]
                exp_obj2(f, amesh, base, base2)
            for eli in range(len(obj.ellipdoids)):
                exp_obj2(f, sphere, base, base2)
        index += 1
    f.close()


