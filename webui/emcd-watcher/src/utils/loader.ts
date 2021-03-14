import { emitter } from '@/utils/bus';

export function showLoader() {
    emitter.emit('show-loader')
}

export function hideLoader() {
    emitter.emit('hide-loader')
}

export async function throughLoader(func: () => any) {
    showLoader()
    console.log('show-loader')
    func()
    console.log('func-ok')
    hideLoader()
    console.log('hide-loader')
}
