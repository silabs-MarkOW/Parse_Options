import sys
import getopt
import shutil

class CliParser :
    def __init__(self) :
        self.long_opts = ['version']
        self.options = {}
        self.option_types = {}
        self.option_params = {}
        self.option_desc = {'version':'show version from git info'}

    def add_option(self,name, datatype=None, default=None, params=None, desc=None) :
        option = name
        if None != datatype :
            option += '='
            if None == params :
                raise RuntimeError('option "%s" missing params'%(name))
            else :
                self.option_params[name] = params
        self.long_opts.append(option)
        if None != default :
            if type(default) != datatype :
                raise RuntimeError('type(%s) != %s'%(default.__str__(),str(datatype)))
            self.options[name] = default
        self.option_types[name] = datatype
        if None != desc :
            self.option_desc[name] = desc

    def format(self,s,width) :
        length = len(s)
        if length <= width : return [s]
        lines = []
        tokens = s.split()
        current = tokens.pop(0)
        while len(tokens) :
            if len(current) + 1 + len(tokens[0]) > width :
                lines.append(current)
                current = tokens.pop(0)
            else :
                current += ' ' + tokens.pop(0)
        lines.append(current)
        return lines

    def exit_help(self, msg = None) :
        width = shutil.get_terminal_size((80, 20))[0]
        if None != msg :
            print('Error: %s'%(msg))
        print('Usage: %s [ options ] <base-filename>\n  options:'%(sys.argv[0]))
        optlen = 0
        paramlen = 0
        for option in self.long_opts :
            if '=' == option[-1] :
                name = option[:-1]
            else :
                name = option
            params = self.option_params.get(name)
            if None != params and len(params) > paramlen : paramlen = len(params)
            if len(option) > optlen : optlen = len(option)
        fmt = '    %%%ds%%-%ds %%s'%(optlen+2,paramlen)
        for option in self.long_opts :
            if '=' == option[-1] :
                name = option[:-1]
            else :
                name = option
                option += ' '
            desc = self.option_desc.get(name)
            if None == desc : desc = ''
            desc = self.format(desc,width-len(fmt%('','','')))
            params = self.option_params.get(name)
            if None == params : params = ''
            print(fmt%('--'+option,params,desc[0]))
            for d in desc[1:] :
                print(fmt%('','',d))
        quit()

    def parse(self) :
        opts,params = getopt.getopt(sys.argv[1:],'hv',self.long_opts)
        for opt,param in opts :
            if '-h' == opt :
                self.exit_help()
            elif '-v' == opt or '--version' == opt :
                print(s2b_get_version())
                quit()
            else :
                for option in self.long_opts :
                    if '=' == option[-1] :
                        name = option[:-1]
                        if '--'+name == opt :
                            datatype = self.option_types[name]
                            if tuple == type(datatype) :
                                tokens = param.split(',')
                                if len(tokens) != len(datatype) :
                                    self.exit_help('tuple length mismatch parsing "%s" parameters.  Expecting %s, got %s'%(opt,datatype.__str__(),tokens.__str__()))
                                option = ()
                                for i in range(len(tokens)) :
                                    option += (datatype[i](tokens[i]),)
                                self.options[name] = option
                            else :
                                self.options[name] = datatype(param)
        print(params)
        print(self.options)
        return self.options,params
    
